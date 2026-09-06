import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty


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
    pass_beauty: BoolProperty(name="Beauty", default=True)
    pass_line: BoolProperty(name="Line", default=False)
    pass_shadow: BoolProperty(name="Shadow", default=False)
    pass_depth: BoolProperty(name="Depth", default=False)

    language: EnumProperty(
        name="UI Language",
        items=(("EN", "English", "English"), ("JA", "日本語", "Japanese")),
        default="EN",
    )

    last_package_path: StringProperty(name="Last Package", default="", options={"HIDDEN"})
