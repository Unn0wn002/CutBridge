from pathlib import Path


def replace_once(path, old, new, label):
    text = path.read_text(encoding="utf-8")
    if old in text:
        if text.count(old) != 1:
            raise RuntimeError(f"{label}: expected one repair anchor, found {text.count(old)}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        print(f"repaired: {label}")
        return
    if new in text:
        print(f"already repaired: {label}")
        return
    raise RuntimeError(f"{label}: neither original nor repaired anchor found")


root = Path(__file__).resolve().parents[1]

qc = root / "apps/after-effects/qc_plus.js"
replace_once(
    qc,
    '    var SCOPE_ORDER = {\n        package: 0,\n',
    '    var SCOPE_ORDER = {\n        "package": 0,\n',
    "qc_plus reserved package key",
)

revision = root / "apps/after-effects/revision_manager.js"
replace_once(
    revision,
    '        return {status: errors.length ? "incompatible" : warnings.length ? "warning" : "safe",\n            reasons: errors, warnings: warnings};\n',
    '        var status;\n'
    '        if (errors.length > 0) {\n'
    '            status = "incompatible";\n'
    '        } else if (warnings.length > 0) {\n'
    '            status = "warning";\n'
    '        } else {\n'
    '            status = "safe";\n'
    '        }\n'
    '        return {status: status, reasons: errors, warnings: warnings};\n',
    "revision compatibility status",
)

pytest_file = root / "tests/test_ae_s7.py"
text = pytest_file.read_text(encoding="utf-8")
marker = "def test_s7_native_after_effects_parser_regressions():"
if marker not in text:
    addition = '''


def test_s7_native_after_effects_parser_regressions():
    root = Path(__file__).resolve().parents[1]
    qc_source = (root / "apps/after-effects/qc_plus.js").read_text(encoding="utf-8")
    revision_source = (root / "apps/after-effects/revision_manager.js").read_text(encoding="utf-8")

    # AE 26.3 ExtendScript rejects an unquoted reserved `package` key.
    assert '        "package": 0,' in qc_source
    assert "\\n        package: 0," not in qc_source

    # AE 26.3 evaluated the previous nested ternary as warning for errors=1/warnings=0.
    # Keep the compatibility decision explicit and parser-safe.
    assert 'if (errors.length > 0) {' in revision_source
    assert 'status = "incompatible";' in revision_source
    assert 'else if (warnings.length > 0) {' in revision_source
    assert 'errors.length ? "incompatible" : warnings.length ? "warning" : "safe"' not in revision_source
'''
    pytest_file.write_text(text.rstrip() + addition.rstrip() + "\n", encoding="utf-8")
    print("added: native AE parser regression test")
else:
    print("already present: native AE parser regression test")
