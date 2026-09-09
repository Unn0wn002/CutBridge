from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one repair anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# B2: narrow Blender N-panel must not compress identity/value controls into
# multi-property rows. Give labels and editable values their own full-width rows.
ui = ROOT / "apps/blender/cutbridge/ui.py"
replace_once(
    ui,
    '''        language_row = layout.row(align=True)\n        language_row.prop(s, "language", text=tr(language, "language"))\n\n        box = layout.box()\n        box.label(text=tr(language, "project_setup"))\n        box.prop(s, "project", text=tr(language, "project"))\n        row = box.row(align=True)\n        row.prop(s, "episode", text=tr(language, "episode"))\n        row.prop(s, "scene_id", text=tr(language, "scene"))\n        row = box.row(align=True)\n        row.prop(s, "cut", text=tr(language, "cut"))\n        row.prop(s, "take", text=tr(language, "take"))\n        row.prop(s, "version", text=tr(language, "version"))\n''',
    '''        def labeled_prop(container, data, property_name, label_text):\n            # Labels and editable values use separate full-width rows so core\n            # identifiers remain readable in a practical narrow N-panel.\n            container.label(text=label_text)\n            container.prop(data, property_name, text="")\n\n        labeled_prop(layout, s, "language", tr(language, "language"))\n\n        box = layout.box()\n        box.label(text=tr(language, "project_setup"))\n        labeled_prop(box, s, "project", tr(language, "project"))\n        labeled_prop(box, s, "episode", tr(language, "episode"))\n        labeled_prop(box, s, "scene_id", tr(language, "scene"))\n        labeled_prop(box, s, "cut", tr(language, "cut"))\n        labeled_prop(box, s, "take", tr(language, "take"))\n        labeled_prop(box, s, "version", tr(language, "version"))\n''',
)
replace_once(
    ui,
    '''        box = layout.box()\n        box.label(text=tr(language, "pass_package"))\n        row = box.row(align=True)\n        row.prop(s, "pass_beauty", text=tr(language, "beauty"))\n        row.prop(s, "pass_line", text=tr(language, "line"))\n        row.prop(s, "pass_shadow", text=tr(language, "shadow"))\n        row = box.row(align=True)\n        row.prop(s, "pass_depth", text=tr(language, "depth"))\n        row.prop(s, "image_format", text=tr(language, "sequence_format"))\n\n        box = layout.box()\n        box.label(text=tr(language, "export"))\n        box.prop(s, "output_dir", text=tr(language, "package_output"))\n        row = box.row(align=True)\n        row.operator("cutbridge.validate", text=tr(language, "validate_cut"), icon="CHECKMARK")\n        row.operator("cutbridge.build_package", text=tr(language, "build_package"), icon="PACKAGE")\n''',
    '''        box = layout.box()\n        box.label(text=tr(language, "pass_package"))\n        box.prop(s, "pass_beauty", text=tr(language, "beauty"))\n        box.prop(s, "pass_line", text=tr(language, "line"))\n        box.prop(s, "pass_shadow", text=tr(language, "shadow"))\n        box.prop(s, "pass_depth", text=tr(language, "depth"))\n        labeled_prop(box, s, "image_format", tr(language, "sequence_format"))\n\n        box = layout.box()\n        box.label(text=tr(language, "export"))\n        labeled_prop(box, s, "output_dir", tr(language, "package_output"))\n        box.operator("cutbridge.validate", text=tr(language, "validate_cut"), icon="CHECKMARK")\n        box.operator("cutbridge.build_package", text=tr(language, "build_package"), icon="PACKAGE")\n''',
)

# AE7: the built-in fallback contains only English strings. It must therefore
# expose EN as the effective locale even when app.settings persisted JA.
ae = ROOT / "apps/after-effects/CutBridge.jsx"
replace_once(
    ae,
    '''            DEFAULT_LOCALE: "EN", FALLBACK_LOCALE: "EN",\n            normalizeLocale: function(value) { return String(value || "").toUpperCase() === "JA" ? "JA" : "EN"; },\n            tr: function(value, key, values) { return format(strings[key] || key, values); },\n            setLocale: function(value) { locale = String(value || "").toUpperCase() === "JA" ? "JA" : "EN"; return locale; },\n''',
    '''            DEFAULT_LOCALE: "EN", FALLBACK_LOCALE: "EN",\n            normalizeLocale: function(value) { return "EN"; },\n            tr: function(value, key, values) { return format(strings[key] || key, values); },\n            setLocale: function(value) { locale = "EN"; return locale; },\n''',
)
replace_once(
    ae,
    '''        function refreshLocale() {\n            localeLabel.text = tr("language_label"); status.text = packageStatusText(state.manifest);\n''',
    '''        function refreshLocale() {\n            // Keep the visible selector synchronized with the effective locale.\n            // This matters when localization.js is missing and fallback can only\n            // provide English even if app.settings previously stored JA.\n            localeSelect.selection = currentLocale === "JA" ? 0 : 1;\n            localeLabel.text = tr("language_label"); status.text = packageStatusText(state.manifest);\n''',
)

# Regression: missing sidecar + persisted JA must render coherent English UI.
ae_test = ROOT / "tests/ae_s8_native_ui_binding_checks.cjs"
anchor = "for (const text of makeRuntime().buttonTexts()) assert.doesNotMatch(text, /\\s \\/ \\s/, 'S8 must not use decorative slash-bilingual buttons');\n"
insert = '''{\n  const h = makeRuntime({injectLocalization: false, savedLocale: 'JA'});\n  assert.equal(h.dropdown().selection.index, 1, 'persisted JA must not remain visibly selected when only English fallback strings are available');\n  assert.deepEqual(h.buttonTexts(), ['1. Import Package', '2. Build Comp', '3. Run QC', '4. Update Revision']);\n  assert.equal(h.projectMutationCount(), 0, 'persisted-locale fallback must remain UX-only');\n}\n\n''' + anchor
replace_once(ae_test, anchor, insert)

# Regression: core editable Blender identifiers/actions must not be compressed
# into shared horizontal rows at narrow sidebar widths.
blender_test = ROOT / "tests/test_s8_blender_localization.py"
with blender_test.open("a", encoding="utf-8") as fh:
    fh.write('''\n\ndef test_blender_panel_uses_narrow_safe_full_width_identity_controls():\n    source = (BLENDER / "ui.py").read_text(encoding="utf-8")\n    assert "def labeled_prop" in source\n    for property_name in ("language", "project", "episode", "scene_id", "cut", "take", "version", "image_format", "output_dir"):\n        assert f'"{property_name}"' in source\n    assert 'row.prop(s, "episode"' not in source\n    assert 'row.prop(s, "scene_id"' not in source\n    assert 'row.prop(s, "cut"' not in source\n    assert 'row.prop(s, "take"' not in source\n    assert 'row.prop(s, "version"' not in source\n    assert 'row.operator("cutbridge.validate"' not in source\n    assert 'row.operator("cutbridge.build_package"' not in source\n''')

print("S8 native defect repair applied")
