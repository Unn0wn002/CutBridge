import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLENDER = ROOT / "apps" / "blender" / "cutbridge"

REQUIRED_TOPICS = {
    "beauty",
    "line",
    "shadow",
    "depth",
    "sequence_format",
    "studio_preset",
    "validate",
    "build",
    "version",
    "camera",
    "output_path",
    "three_d_handoff",
}


def _help_content_literal():
    tree = ast.parse((BLENDER / "help_content.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "HELP_CONTENT" for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("HELP_CONTENT assignment not found")


def test_context_help_has_required_en_ja_topics_and_sections():
    content = _help_content_literal()
    assert REQUIRED_TOPICS <= set(content)
    for topic in REQUIRED_TOPICS:
        assert set(content[topic]) == {"EN", "JA"}
        for language in ("EN", "JA"):
            title, sections = content[topic][language]
            assert title.strip()
            assert len(sections) >= 3
            assert all(str(heading).strip() and str(body).strip() for heading, body in sections)


def test_context_help_operator_is_registered_and_uses_localized_content():
    init_source = (BLENDER / "__init__.py").read_text(encoding="utf-8")
    operator_source = (BLENDER / "help_ops.py").read_text(encoding="utf-8")
    assert "CUTBRIDGE_OT_ContextHelp" in init_source
    assert 'bl_idname = "cutbridge.context_help"' in operator_source
    assert "get_help(self.topic, language)" in operator_source
    assert "invoke_popup" in operator_source


def test_main_panel_exposes_contextual_help_without_enabling_hidden_3d_control():
    source = (BLENDER / "ui.py").read_text(encoding="utf-8")
    assert 'operator("cutbridge.context_help"' in source
    for topic in (
        "beauty",
        "line",
        "shadow",
        "depth",
        "sequence_format",
        "studio_preset",
        "validate",
        "build",
        "version",
        "camera",
        "output_path",
    ):
        assert f'"{topic}"' in source
    # Experimental producer-only 3D handoff remains intentionally hidden.
    assert "handoff_3d_enabled" not in source
