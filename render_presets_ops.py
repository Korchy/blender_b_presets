# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_b_presets

import bpy
from bpy.props import IntProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .render_presets import RenderPresets
from .render_presets_batch_render import BatchRender


class RENDER_PRESETS_OT_add_new_preset(Operator):
    bl_idname = 'render_presets.add_new_preset'
    bl_label = 'Add new preset'
    bl_description = 'B-Presets: Add new preset'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # create new preset
        RenderPresets.add_new_preset(context=context)
        return {'FINISHED'}


class RENDER_PRESETS_OT_remove_active_preset(Operator):
    bl_idname = 'render_presets.remove_active_preset'
    bl_label = 'Remove active preset'
    bl_description = 'B-Presets: Remove active preset'
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


class RENDER_PRESETS_OT_reload_presets(Operator):
    bl_idname = 'render_presets.reload_presets'
    bl_label = 'Reload presets'
    bl_description = 'B-Presets: Reload presets'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # reload presets list from files
        RenderPresets.load_presets_list(context=context)
        return {'FINISHED'}


class RENDER_PRESETS_OT_scene_to_preset(Operator):
    bl_idname = 'render_presets.scene_to_preset'
    bl_label = 'Save scene to active preset'
    bl_description = 'B-Presets: Save current scene settings to preset'
    bl_options = {'REGISTER'}

    def execute(self, context):
        # scene to active preset
        RenderPresets.scene_to_preset(
            context=context,
            preset=context.window_manager.render_presets_presets[context.window_manager.render_presets_active_preset]
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if 0 <= context.window_manager.render_presets_active_preset < len(context.window_manager.render_presets_presets)\
                and not context.window_manager.render_presets_presets[context.window_manager.render_presets_active_preset].locked:
            return True
        else:
            return False


class RENDER_PRESETS_OT_preset_to_scene(Operator):
    bl_idname = 'render_presets.preset_to_scene'
    bl_label = 'Load preset settings to scene'
    bl_description = 'B-Presets: Load settings from active preset to the scene'
    bl_options = {'REGISTER'}

    preset_id: IntProperty(
        default=-1
    )

    def execute(self, context):
        # preset to scene
        active_preset_id = context.window_manager.render_presets_active_preset
        if active_preset_id != self.preset_id:
            context.window_manager.render_presets_active_preset = self.preset_id
        RenderPresets.preset_to_scene(
            context=context,
            preset=context.window_manager.render_presets_presets[context.window_manager.render_presets_active_preset]
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if 0 <= context.window_manager.render_presets_active_preset < len(context.window_manager.render_presets_presets):
            return True
        else:
            return False


class RENDER_PRESETS_OT_render_checked_presets(Operator):
    bl_idname = 'render_presets.render_checked_presets'
    bl_label = 'Render with marked presets'
    bl_description = 'B-Presets: Render scene with all marked presets'
    bl_options = {'REGISTER'}

    def execute(self, context):
        # render with checked presets
        BatchRender.batch_render_with_presets(
            context=context,
            presets=[preset for preset in context.window_manager.render_presets_presets if preset.checked]
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if len(context.window_manager.render_presets_presets) > 0\
                and next((preset for preset in context.window_manager.render_presets_presets if preset.checked), None):
            return True
        else:
            return False


class RENDER_PRESETS_OT_restore_from_backup(Operator):
    bl_idname = 'render_presets.restore_from_backup'
    bl_label = 'Restore scene'
    bl_description = 'B-Presets: Restore scene'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # restore scene from backup
        RenderPresets.restore_scene(
            context=context
        )
        return {'FINISHED'}


def register():
    register_class(RENDER_PRESETS_OT_add_new_preset)
    register_class(RENDER_PRESETS_OT_remove_active_preset)
    register_class(RENDER_PRESETS_OT_reload_presets)
    register_class(RENDER_PRESETS_OT_preset_to_scene)
    register_class(RENDER_PRESETS_OT_scene_to_preset)
    register_class(RENDER_PRESETS_OT_render_checked_presets)
    register_class(RENDER_PRESETS_OT_restore_from_backup)


def unregister():
    unregister_class(RENDER_PRESETS_OT_restore_from_backup)
    unregister_class(RENDER_PRESETS_OT_render_checked_presets)
    unregister_class(RENDER_PRESETS_OT_scene_to_preset)
    unregister_class(RENDER_PRESETS_OT_preset_to_scene)
    unregister_class(RENDER_PRESETS_OT_reload_presets)
    unregister_class(RENDER_PRESETS_OT_remove_active_preset)
    unregister_class(RENDER_PRESETS_OT_add_new_preset)
