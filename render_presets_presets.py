# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import bpy
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty
from bpy.types import PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class
from .render_presets import RenderPresets


class RENDER_PRESETS_presets_list(PropertyGroup):

    name: StringProperty()

    checked: BoolProperty(
        default=False
    )

    locked: BoolProperty(
        default=False,
        update=lambda self, context: RenderPresets.change_preset_lock(
            context=context,
            preset_name=self.name,
            lock_status=self.locked
        )
    )


def register():
    register_class(RENDER_PRESETS_presets_list)
    WindowManager.render_presets_presets = CollectionProperty(type=RENDER_PRESETS_presets_list)
    WindowManager.render_presets_active_preset = IntProperty(
        name='active preset',
        default=0
    )
    RenderPresets.load_presets_list(context=bpy.context)


def unregister():
    RenderPresets.clear_presets_list(context=bpy.context)
    del WindowManager.render_presets_active_preset
    del WindowManager.render_presets_presets
    unregister_class(RENDER_PRESETS_presets_list)