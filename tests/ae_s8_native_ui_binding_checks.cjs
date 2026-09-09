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
  if (savedLocale) settingsStore['CutBridge:ui_locale'] = savedLocale;
  let projectMutationCount = 0;

  function Window() {
    this.layout = {resize() {}, layout() {}};
    this.orientation = '';
    this.alignChildren = [];
    this.spacing = 0;
    this.margins = 0;
  }
  Window.prototype.add = function(type, unused, textOrItems) {
    const control = {
      type,
      text: Array.isArray(textOrItems) ? '' : String(textOrItems == null ? '' : textOrItems),
      items: Array.isArray(textOrItems) ? textOrItems.map((text, index) => ({text, index})) : [],
      graphics: {font: {name: 'Arial'}},
      preferredSize: {},
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
    controls.push(control);
    return control;
  };
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
    alert() {},
    confirm() { return false; },
    $: {writeln() {}}
  };
  if (injectLocalization) runtime.CutBridgeLocalization = Localization;
  vm.createContext(runtime);
  vm.runInContext(source, runtime);

  return {
    controls,
    settingsStore,
    projectMutationCount: () => projectMutationCount,
    buttonTexts: () => controls.filter((item) => item.type === 'button').map((item) => item.text),
    statusText: () => controls.find((item) => item.type === 'statictext' && /package|パッケージ/.test(item.text))?.text,
    dropdown: () => controls.find((item) => item.type === 'dropdownlist')
  };
}

{
  const h = makeRuntime();
  const dropdown = h.dropdown();
  assert.ok(dropdown, 'S8 panel must expose an explicit locale dropdown');
  assert.equal(dropdown.selection.index, 0, 'Japanese must be selected by default when S8 localization is available');
  assert.deepEqual(h.buttonTexts(), ['1. パッケージ読み込み', '2. コンポ作成', '3. QC実行', '4. 差し替え']);
  assert.equal(h.statusText(), 'パッケージ未読み込み');
  assert.equal(h.projectMutationCount(), 0, 'locale initialization must not mutate project state');

  dropdown.selection = 1;
  dropdown.onChange();
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.equal(h.settingsStore['CutBridge:ui_locale'], 'EN');
  assert.equal(h.projectMutationCount(), 0, 'locale switch must not mutate project state');
}

{
  const h = makeRuntime({savedLocale: 'EN'});
  assert.equal(h.dropdown().selection.index, 1, 'saved English preference must be restored');
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.equal(h.projectMutationCount(), 0);
}

{
  const h = makeRuntime({injectLocalization: false});
  assert.equal(h.dropdown().selection.index, 1, 'missing localization sidecar must fall back to English');
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.equal(h.projectMutationCount(), 0, 'fallback must remain UX-only');
}

for (const text of makeRuntime().buttonTexts()) assert.doesNotMatch(text, /\s\/\s/, 'S8 must not use decorative slash-bilingual buttons');

{
  const h = makeRuntime({injectLocalization: false, savedLocale: 'JA'});
  assert.equal(h.dropdown().selection.index, 1, 'persisted JA must not remain visibly selected when only English fallback strings are available');
  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);
  assert.equal(h.projectMutationCount(), 0, 'persisted-locale fallback must remain UX-only');
}

console.log('S8 native ScriptUI localization binding: PASS (JA default, EN switch/persistence, safe fallback, non-mutation)');
