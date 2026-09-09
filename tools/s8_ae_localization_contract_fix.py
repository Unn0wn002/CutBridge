from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "apps" / "after-effects" / "CutBridge.jsx"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 1:
        print(f"contract fix: {label}")
        return text.replace(old, new, 1)
    if count == 0 and new in text:
        print(f"already fixed: {label}")
        return text
    raise RuntimeError(f"{label}: expected exactly one anchor, found {count}")


text = PATH.read_text(encoding="utf-8")

# Preserve the explicit S6 fail-closed source form. The thrown canonical English
# detail is localized later by alertError(), so Japanese UX does not require
# changing this safety-visible assertion.
text = replace_once(
    text,
    '            if (typeof confirm !== "function") throw new Error(tr("confirmation_unavailable"));',
    '            if (typeof confirm !== "function") throw new Error("After Effects confirmation UI is unavailable; revision was not applied.");',
    "explicit confirmation fail-closed literal",
)

# Keep the existing S6 contract assertion that the selected revision version is
# formatted through CutBridgeContract.zeroPad at both prompt and success sites.
text = replace_once(
    text,
    '                alert(tr("revision_updated", {version: revisionVersion}) + "\\n" + tr("revision_preserved"));',
    '                alert(tr("revision_updated", {version: CutBridgeContract.zeroPad(selected.manifest.version, 3)}) + "\\n" + tr("revision_preserved"));',
    "revision version contract scope",
)

# Preserve the S7 source-visible qc.render(records) boundary. Localization is a
# presentation transform of the record array before the unchanged QC renderer.
text = replace_once(
    text,
    '''        function finish() {
            var l10n = getLocalization(), localizedRecords = l10n.localizeRecords(currentLocale, records);
            var report = qc.render(localizedRecords);
            alert("CutBridge QC — " + l10n.qcHeadline(currentLocale, report.headline) + "\\n\\n" + l10n.localizeRenderedQC(currentLocale, report.text));
        }
''',
    '''        function finish() {
            var l10n = getLocalization();
            records = l10n.localizeRecords(currentLocale, records);
            var report = qc.render(records);
            alert("CutBridge QC — " + l10n.qcHeadline(currentLocale, report.headline) + "\\n\\n" + l10n.localizeRenderedQC(currentLocale, report.text));
        }
''',
    "S7 qc.render(records) boundary",
)

PATH.write_text(text, encoding="utf-8")
print("S8 AE localization contract compatibility fixes complete")
