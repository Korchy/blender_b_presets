# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .render_presets import RenderPresets


class RENDER_PRESETS_OT_add_new_preset(Operator):
    bl_idname = 'render_presets.add_new_preset'
    bl_label = 'render_presets: add new preset'
    bl_description = 'Render Presets: Add new preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # create new preset
        RenderPresets.add_new_preset(context=context)
        return {'FINISHED'}


def register():
    register_class(RENDER_PRESETS_OT_add_new_preset)


def unregister():
    unregister_class(RENDER_PRESETS_OT_add_new_preset)
