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
if not block.endswith('\n'):
    block += '\n'
updated = source[:start] + block + source[end:]
if updated == source:
    raise SystemExit('AE UI replacement produced no change')
jsx.write_text(updated, encoding='utf-8')

shutil.copyfile(ORCH / 'ae_s8_native_ui_binding_checks.cjs', ROOT / 'tests' / 'ae_s8_native_ui_binding_checks.cjs')
shutil.copyfile(ORCH / 'test_ae_beta2_panel_ux.py', ROOT / 'tests' / 'test_ae_beta2_panel_ux.py')
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
