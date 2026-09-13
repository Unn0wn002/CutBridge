const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'apps/after-effects/CutBridge.jsx'), 'utf8');
const Localization = require(path.join(root, 'apps/after-effects/localization.js'));

function makeRuntime({injectLocalization = true, savedLocale = null} = {}) {
  const controls = [];
  const settingsStore = {};
  const alerts = [];
  if (savedLocale) settingsStore['CutBridge:ui_locale'] = savedLocale;
  let projectMutationCount = 0;

  function attachContainerApi(control) {
    control.add = function(type, unused, textOrItems) { return makeControl(type, textOrItems); };
    return control;
  }

  function makeControl(type, textOrItems) {
    const control = {
      type,
      text: Array.isArray(textOrItems) ? '' : String(textOrItems == null ? '' : textOrItems),
      items: Array.isArray(textOrItems) ? textOrItems.map((text, index) => ({text, index})) : [],
      graphics: {font: {name: 'Arial'}},
      preferredSize: {},
      alignment: null,
      alignChildren: [],
      orientation: '',
      spacing: 0,
      margins: 0,
      onClick: null,
      onChange: null
    };
    let selection = null;
    Object.defineProperty(control, 'selection', {
      get() { return selection; },
      set(value) {
        if (typeof value === 'number') selection = control.items[value] || null;
        else selection = value;
      }
    });
    if (type === 'group' || type === 'panel') attachContainerApi(control);
    controls.push(control);
    return control;
  }

  function Window() {
    this.layout = {resize() {}, layout() {}};
    this.orientation = '';
    this.alignChildren = [];
    this.spacing = 0;
    this.margins = 0;
  }
  Window.prototype.add = function(type, unused, textOrItems) { return makeControl(type, textOrItems); };
  Window.prototype.center = function() {};
  Window.prototype.show = function() {};
  function Panel() {}

  const app = {
    settings: {
      haveSetting(section, key) { return Object.prototype.hasOwnProperty.call(settingsStore, `${section}:${key}`); },
      getSetting(section, key) { return settingsStore[`${section}:${key}`]; },
      saveSetting(section, key, value) { settingsStore[`${section}:${key}`] = String(value); }
    }
  };
  Object.defineProperty(app, 'project', {
    get() { return null; },
    set() { projectMutationCount++; }
  });

  const runtime = {
    Window,
    Panel,
    ScriptUI: {newFont() { return {}; }},
    app,
    alert(message) { alerts.push(String(message)); },
    confirm() { return false; },
    $: {writeln() {}}
  };
  if (injectLocalization) runtime.CutBridgeLocalization = Localization;
  vm.createContext(runtime);
  vm.runInContext(source, runtime);

  return {
    controls,
    alerts,
    settingsStore,
    projectMutationCount: () => projectMutationCount,
    buttonTexts: () => controls.filter((item) => item.type === 'button' && item.text !== '?').map((item) => item.text),
    helpButtons: () => controls.filter((item) => item.type === 'button' && item.text === '?'),
    staticTexts: () => controls.filter((item) => item.type === 'statictext').map((item) => item.text),
    panels: () => controls.filter((item) => item.type === 'panel'),
    dropdown: () => controls.find((item) => item.type === 'dropdownlist')
  };
}

{
  const h = makeRuntime();
  const dropdown = h.dropdown();
  assert.ok(dropdown, 'AE panel must expose an explicit locale dropdown');
  assert.equal(dropdown.selection.index, 0, 'Japanese must be selected by default');
  assert.deepEqual(h.buttonTexts(), ['1. パッケージ読み込み', '2. コンポ作成', '3. QC実行', '4. 差し替え']);
  assert.equal(h.helpButtons().length, 4, 'each primary AE action must have contextual ? help');
  assert.equal(h.panels().length, 2, 'beta.2 AE UX must separate package/status from workflow actions');
  assert.ok(h.staticTexts().some((text) => text.includes('状態: 警告 / WARNING')), 'initial status hierarchy must be visible');
  assert.ok(h.staticTexts().some((text) => text.includes('読み込みだけではAEプロジェクトのBuildや変更は行いません')), 'Load description must explain consequence');
  assert.equal(h.projectMutationCount(), 0, 'opening the panel must not mutate project state');

  h.helpButtons()[0].onClick();
  assert.equal(h.alerts.length, 1, 'context help must be available on demand');
  assert.match(h.alerts[0], /パッケージ読み込み/);
  assert.equal(h.projectMutationCount(), 0, 'opening contextual help must not mutate project state');

  dropdown.selection = 1;
  dropdown.onChange();
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.equal(h.settingsStore['CutBridge:ui_locale'], 'EN');
  assert.ok(h.staticTexts().some((text) => text.includes('Status: WARNING')), 'English status hierarchy must refresh');
  assert.ok(h.staticTexts().some((text) => text.includes('Loading reads package metadata')), 'English descriptions must refresh');
  assert.equal(h.projectMutationCount(), 0, 'locale switch must remain UX-only');
}

{
  const h = makeRuntime({savedLocale: 'EN'});
  assert.equal(h.dropdown().selection.index, 1, 'saved English preference must be restored');
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.equal(h.helpButtons().length, 4);
  assert.equal(h.projectMutationCount(), 0);
}

{
  const h = makeRuntime({injectLocalization: false});
  assert.equal(h.dropdown().selection.index, 1, 'missing localization sidecar must fall back to English');
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.ok(h.staticTexts().some((text) => text.includes('Status: WARNING')));
  assert.equal(h.projectMutationCount(), 0, 'fallback must remain UX-only');
}

for (const text of makeRuntime().buttonTexts()) assert.doesNotMatch(text, /\s\/\s/, 'AE UI must not use decorative slash-bilingual primary buttons');

console.log('S8/beta.2 native ScriptUI binding: PASS (dockable hierarchy, EN/JA descriptions, contextual help, non-mutation)');
