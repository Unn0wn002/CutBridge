from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
AE = ROOT / "apps" / "after-effects"


def _run_node(script_name: str) -> None:
    node = shutil.which("node")
    assert node, "Node is required for S8 After Effects checks"
    subprocess.run([node, str(ROOT / "tests" / script_name)], cwd=ROOT, check=True)


def test_ae_s8_localization_engine():
    _run_node("ae_s8_localization_checks.cjs")


def test_ae_s8_native_scriptui_binding():
    _run_node("ae_s8_native_ui_binding_checks.cjs")


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
    assert "qc.render(records)" in source
    assert 'if (typeof confirm !== "function") throw new Error("After Effects confirmation UI is unavailable; revision was not applied.");' in source
    assert "CutBridge / カットブリッジ" not in source
    assert "Import Package / 読み込み" not in source
