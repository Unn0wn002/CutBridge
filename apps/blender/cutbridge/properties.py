import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty


def _default_output_dir():
    # Blender's // path keeps the package next to the .blend by default.
    return "//cutbridge_exports"


class CUTBRIDGE_PG_Settings(bpy.types.PropertyGroup):
    project: StringProperty(name="Project", default="PROJECT_A")
    episode: StringProperty(name="Episode", default="EP01")
    scene_id: StringProperty(name="Scene", default="SC010")
    cut: StringProperty(name="Cut", default="C012")
    take: StringProperty(name="Take", default="T01")
    version: IntProperty(name="Version", default=1, min=1)

    output_dir: StringProperty(
        name="Package Output",
        description="Directory where CutBridge packages will be created",
        subtype="DIR_PATH",
        default=_default_output_dir(),
    )

    studio_preset_mode: EnumProperty(
        name="Studio Preset Mode",
        description="Manual keeps legacy controls; Default uses CutBridge's safe built-in preset; Custom loads one validated JSON preset",
        items=(
            ("MANUAL", "Manual", "Use the existing CutBridge pass/format controls"),
            ("DEFAULT", "CutBridge Default", "Use the built-in safe CutBridge studio preset"),
            ("CUSTOM", "Custom JSON", "Load one validated data-only studio preset JSON file"),
        ),
        default="MANUAL",
    )

    studio_preset_path: StringProperty(
        name="Studio Preset JSON",
        description="Optional custom CutBridge studio preset JSON file. Presets are declarative data only and are validated before use",
        subtype="FILE_PATH",
        default="",
    )

    image_format: EnumProperty(
        name="Sequence Format",
        items=(
            ("PNG", "PNG", "PNG image sequence"),
            ("OPEN_EXR", "OpenEXR", "OpenEXR image sequence"),
            ("TIFF", "TIFF", "TIFF image sequence"),
        ),
        default="PNG",
    )

    # BEAUTY has a renderer-independent Combined/Image source. Other logical
    # passes are opt-in because their availability depends on the active engine
    # and View Layer; CutBridge validates them instead of silently guessing.
    # These properties remain authoritative in MANUAL preset mode.
    pass_beauty: BoolProperty(name="Beauty", default=True)
    pass_line: BoolProperty(name="Line", default=False)
    pass_shadow: BoolProperty(name="Shadow", default=False)
    pass_depth: BoolProperty(name="Depth", default=False)

    # S10B producer setting. It intentionally remains off and is not exposed as
    # a normal user-facing workflow until native AE reconstruction is validated.
    handoff_3d_enabled: BoolProperty(
        name="3D Handoff Data",
        description="Write experimental producer-only camera/null samples into cutbridge.json. Current AE import does not create camera/null layers",
        default=False,
    )
    handoff_3d_pixels_per_blender_unit: FloatProperty(
        name="3D Handoff Pixels Per Blender Unit",
        description="Explicit spatial scale for mapping Blender world units into AE composition pixels",
        default=100.0,
        min=0.001,
        max=1_000_000.0,
    )

    language: EnumProperty(
        name="UI Language",
        description="CutBridge display language. Stable package data and diagnostic codes are never translated",
        items=(("JA", "日本語", "Japanese"), ("EN", "English", "English")),
        default="JA",
    )

    last_package_path: StringProperty(name="Last Package", default="", options={"HIDDEN"})
