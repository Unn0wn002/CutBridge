from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
AE = ROOT / "apps" / "after-effects"


def test_ae_s8_localization_engine():
    node = shutil.which("node")
    assert node, "Node is required for S8 After Effects localization checks"
    subprocess.run([node, str(ROOT / "tests" / "ae_s8_localization_checks.cjs")], cwd=ROOT, check=True)


def test_ae_s8_localization_sidecar_is_host_independent_and_parser_safe():
    source = (AE / "localization.js").read_text(encoding="utf-8")
    assert "CutBridgeLocalization" in source
    assert 'DEFAULT_LOCALE = "JA"' in source
    assert 'FALLBACK_LOCALE = "EN"' in source
    assert "CBQ-COMP-DRIFT-FRAME-RATE" in source
    assert "app.project" not in source
    assert "replaceSource(" not in source
    assert "items.addFolder" not in source
    assert "layers.add(" not in source


def test_ae_s8_panel_binding_contract_is_present_after_native_patch():
    source = (AE / "CutBridge.jsx").read_text(encoding="utf-8")
    # These anchors are populated by the guarded S8 JSX patch. Keeping the test
    # here makes the branch fail closed until the native panel actually binds the
    # localization engine rather than merely shipping an unused dictionary.
    assert "function getLocalization()" in source
    assert '"/localization.js"' in source
    assert "CutBridgeLocalization" in source
    assert "loadLocalePreference" in source
    assert "saveLocalePreference" in source
    assert 'pal.add("dropdownlist"' in source
    assert 'tr("import_package")' in source
    assert 'tr("build_comp")' in source
    assert 'tr("run_qc")' in source
    assert 'tr("update_revision")' in source
    assert "localizeRecords" in source
    assert "formatRevisionBlocked" in source
    assert "CutBridge / カットブリッジ" not in source
    assert "Import Package / 読み込み" not in source
