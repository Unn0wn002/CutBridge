from __future__ import annotations

import textwrap

import bpy
from bpy.props import StringProperty

from .help_content import get_help


class CUTBRIDGE_OT_ContextHelp(bpy.types.Operator):
    bl_idname = "cutbridge.context_help"
    bl_label = "CutBridge Help"
    bl_description = "Show contextual CutBridge help for this control"
    bl_options = {"INTERNAL"}

    topic: StringProperty(name="Topic", default="validate", options={"HIDDEN"})

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=460)

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        language = getattr(context.scene.cutbridge, "language", "EN")
        title, sections = get_help(self.topic, language)
        layout = self.layout
        layout.label(text=title, icon="QUESTION")
        for heading, body in sections:
            box = layout.box()
            box.label(text=heading)
            for line in textwrap.wrap(str(body), width=62, break_long_words=True, break_on_hyphens=False) or [""]:
                box.label(text=line)
