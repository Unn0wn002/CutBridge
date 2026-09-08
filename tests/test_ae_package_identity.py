"""Run AE producer/consumer package identity regressions in the complete pytest suite."""
from pathlib import Path
import ast
import json
import re
import shutil
import subprocess
from types import SimpleNamespace


def test_ae_package_name_binds_logical_identity():
    node = shutil.which("node")
    assert node, "Node is required for After Effects package identity regression tests"
    root = Path(__file__).resolve().parents[1]
    subprocess.run(
        [node, str(root / "tests" / "ae_package_identity_checks.cjs")],
        cwd=root,
        check=True,
    )


def test_ae_identity_matches_executable_python_producer():
    """Use the real producer functions without requiring bpy in static CI."""
    root = Path(__file__).resolve().parents[1]
    path = root / "apps/blender/cutbridge/core.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {"safe_token", "version_token", "package_name"}
    selected = [n for n in tree.body if
                isinstance(n, ast.FunctionDef) and n.name in names or
                isinstance(n, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "INVALID_FS_CHARS" for t in n.targets)]
    namespace = {"re": re}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), "exec"), namespace)
    assert names <= namespace.keys()
    # Enumerate Python's actual whitespace set rather than copying the JS table.
    whitespace = [chr(cp) for cp in range(0x110000) if chr(cp).isspace()]
    raw_values = ["Normal009du", "桜🌸", "é", "e\u0301", "\ufeff", "\u180e", "\u200b", 'A<>:"/\\|?*B']
    for w in whitespace:
        raw_values.extend([w + "桜", "桜" + w, w + "桜" + w, "A" + w + w + "B"])
    manifests = []
    for field, attr in [("project", "project"), ("episode", "episode"), ("scene", "scene_id"),
                        ("cut", "cut"), ("take", "take")]:
        for raw in raw_values:
            settings = SimpleNamespace(project="桜", episode="EP01", scene_id="SC010", cut="C001", take="T01", version=1)
            setattr(settings, attr, raw)
            m = dict(schema="cutbridge-manifest", schema_version=1, cutbridge_version="0.2.3",
                     project=settings.project, episode=settings.episode, scene=settings.scene_id,
                     cut=settings.cut, take=settings.take, version=1,
                     package_name=namespace["package_name"](settings), fps=24,
                     frames=dict(start=0, end=2, count=3),
                     resolution=dict(width=1920, height=1080, pixel_aspect=1),
                     passes=[dict(name="BEAUTY", path="render/beauty", sequence_pattern="b####.png", required=True)],
                     ae=dict(comp_name="C001_COMP"))
            manifests.append(m)
    node = shutil.which("node")
    assert node, "Node is required for producer/consumer parity"
    subprocess.run([node, str(root / "tests/ae_package_identity_checks.cjs"), "--producer-cases"],
                   input=json.dumps(manifests, ensure_ascii=True), text=True, encoding="utf-8", cwd=root, check=True)
