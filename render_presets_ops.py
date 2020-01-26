# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import bpy
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


class RENDER_PRESETS_OT_remove_active_preset(Operator):
    bl_idname = 'render_presets.remove_active_preset'
    bl_label = 'render_presets: remove active preset'
    bl_description = 'Render Presets: Remove active preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # remove existed preset
        active_preset_item = context.window_manager.render_presets_presets[context.window_manager.render_presets_active_preset]
        if active_preset_item.locked:
            bpy.ops.render_presets.messagebox('INVOKE_DEFAULT', message='Can\'t remove locked preset!')
        else:
            RenderPresets.remove_preset(context=context, preset=active_preset_item)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if 0 <= context.window_manager.render_presets_active_preset < len(context.window_manager.render_presets_presets):
            return True
        else:
            return False


def register():
    register_class(RENDER_PRESETS_OT_add_new_preset)
    register_class(RENDER_PRESETS_OT_remove_active_preset)


def unregister():
    unregister_class(RENDER_PRESETS_OT_remove_active_preset)
    unregister_class(RENDER_PRESETS_OT_add_new_preset)
