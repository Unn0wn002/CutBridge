from pathlib import Path
import shutil

ROOT = Path.cwd()
ORCH = ROOT.parent / 'orchestrator' / 'orchestration'

jsx = ROOT / 'apps' / 'after-effects' / 'CutBridge.jsx'
source = jsx.read_text(encoding='utf-8')
start_marker = '    function packageStatusText(manifest) {'
end_marker = '    CutBridgeContract.loadManifest = loadManifest;'
start = source.index(start_marker)
end = source.index(end_marker, start)
block = (ORCH / 'beta2_ae_ui_block.txt').read_text(encoding='utf-8')

replacements = [
    (
        '        var localeRow = pal.add("group");\n        localeRow.orientation = "row"; localeRow.alignChildren = ["left", "center"];\n        var localeLabel = localeRow.add("statictext", undefined, tr("language_label"));\n        var localeSelect = localeRow.add("dropdownlist", undefined, ["日本語", "English"]); localeSelect.selection = currentLocale === "JA" ? 0 : 1;\n',
        '        var localeLabel = pal.add("statictext", undefined, tr("language_label"));\n        var localeSelect = pal.add("dropdownlist", undefined, ["日本語", "English"]); localeSelect.selection = currentLocale === "JA" ? 0 : 1;\n'
    ),
    (
        '        var packagePanel = pal.add("panel", undefined, aeUiText("package_section"));\n        packagePanel.orientation = "column"; packagePanel.alignChildren = ["fill", "top"]; packagePanel.spacing = 4; packagePanel.margins = 10;\n        var packageName = packagePanel.add("statictext", undefined, ""); packageName.characters = 48;\n        var packageMeta = packagePanel.add("statictext", undefined, packageStatusText(state.manifest)); packageMeta.characters = 48;\n        var statusKind = packagePanel.add("statictext", undefined, ""); statusKind.characters = 48;\n        var statusDetail = packagePanel.add("statictext", undefined, "", {multiline: true}); statusDetail.characters = 52; statusDetail.preferredSize.height = 34;\n\n        var actionsPanel = pal.add("panel", undefined, aeUiText("actions_section"));\n        actionsPanel.orientation = "column"; actionsPanel.alignChildren = ["fill", "top"]; actionsPanel.spacing = 5; actionsPanel.margins = 10;\n',
        '        var packageHeading = pal.add("statictext", undefined, aeUiText("package_section"));\n        try { packageHeading.graphics.font = ScriptUI.newFont(packageHeading.graphics.font.name, "BOLD", 12); } catch (packageHeadingError) {}\n        var packageName = pal.add("statictext", undefined, ""); packageName.characters = 48;\n        var packageMeta = pal.add("statictext", undefined, packageStatusText(state.manifest)); packageMeta.characters = 48;\n        var statusKind = pal.add("statictext", undefined, ""); statusKind.characters = 48;\n        var statusDetail = pal.add("statictext", undefined, "", {multiline: true}); statusDetail.characters = 52; statusDetail.preferredSize.height = 34;\n\n        var actionsHeading = pal.add("statictext", undefined, aeUiText("actions_section"));\n        try { actionsHeading.graphics.font = ScriptUI.newFont(actionsHeading.graphics.font.name, "BOLD", 12); } catch (actionsHeadingError) {}\n'
    ),
    (
        '        function addAction(buttonText, descriptionKey, helpTopic, handler) {\n            var row = actionsPanel.add("group"); row.orientation = "row"; row.alignChildren = ["fill", "center"];\n            var button = row.add("button", undefined, buttonText); button.alignment = ["fill", "center"];\n            var helpButton = row.add("button", undefined, "?"); helpButton.preferredSize.width = 30;\n            var description = actionsPanel.add("statictext", undefined, aeUiText(descriptionKey), {multiline: true});\n',
        '        function addAction(buttonText, descriptionKey, helpTopic, handler) {\n            var button = pal.add("button", undefined, buttonText);\n            var helpButton = pal.add("button", undefined, "?"); helpButton.preferredSize.width = 30;\n            var description = pal.add("statictext", undefined, aeUiText(descriptionKey), {multiline: true});\n'
    ),
    (
        '            packagePanel.text = aeUiText("package_section");\n            actionsPanel.text = aeUiText("actions_section");\n',
        '            packageHeading.text = aeUiText("package_section");\n            actionsHeading.text = aeUiText("actions_section");\n'
    ),
]

for old, new in replacements:
    if old not in block:
        raise SystemExit('Expected AE UI payload anchor not found')
    block = block.replace(old, new, 1)

if not block.endswith('\n'):
    block += '\n'
updated = source[:start] + block + source[end:]
if updated == source:
    raise SystemExit('AE UI replacement produced no change')
jsx.write_text(updated, encoding='utf-8')

s8_target = ROOT / 'tests' / 'ae_s8_native_ui_binding_checks.cjs'
shutil.copyfile(ORCH / 'ae_s8_native_ui_binding_checks.cjs', s8_target)
s8 = s8_target.read_text(encoding='utf-8')
s8 = s8.replace(
    "  assert.equal(h.panels().length, 2, 'beta.2 AE UX must separate package/status from workflow actions');\n",
    "  assert.ok(h.staticTexts().includes('パッケージ'), 'package section heading must be visible');\n  assert.ok(h.staticTexts().includes('ワークフロー'), 'workflow section heading must be visible');\n"
)
s8_target.write_text(s8, encoding='utf-8')

ux_target = ROOT / 'tests' / 'test_ae_beta2_panel_ux.py'
shutil.copyfile(ORCH / 'test_ae_beta2_panel_ux.py', ux_target)
ux = ux_target.read_text(encoding='utf-8').replace(
    "assert SOURCE.count('row.add(\"button\", undefined, \"?\")') == 1",
    "assert SOURCE.count('pal.add(\"button\", undefined, \"?\")') == 1"
)
ux_target.write_text(ux, encoding='utf-8')

shutil.copyfile(ORCH / 'AE_PANEL_BETA2.md', ROOT / 'docs' / 'AE_PANEL_BETA2.md')

ci = ROOT / '.github' / 'workflows' / 'ci.yml'
text = ci.read_text(encoding='utf-8')
needle = 'tests/test_ae_package_identity.py\n'
replacement = 'tests/test_ae_package_identity.py tests/test_ae_beta2_panel_ux.py\n'
if replacement not in text:
    if needle not in text:
        raise SystemExit('CI pytest subset anchor not found')
    text = text.replace(needle, replacement, 1)
ci.write_text(text, encoding='utf-8')
