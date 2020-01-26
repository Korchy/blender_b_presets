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

    name: StringProperty(
        update=lambda self, context: self.on_name_update(self, context)
    )

    name_old: StringProperty(
        default=''
    )

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

    @staticmethod
    def on_name_update(self, context):
        # on name changed (already changed)
        if self.name != self.name_old and self.name_old != '':
            if self.locked:
                self._restore_name(self, message='Can\'t modify locked preset!')
            elif not self.name:
                self._restore_name(self, message='Empty name!')
            elif context.window_manager.render_presets_presets.keys().count(self.name) > 1:
                self._restore_name(self, message='Name already existed!')
            else:
                RenderPresets.change_preset_name(
                    context=context,
                    preset_item=self
                )
        self.name_old = self.name

    @staticmethod
    def _restore_name(self, message=''):
        # restore name from name_old with showing warning message
        self.name = self.name_old
        bpy.ops.render_presets.messagebox('INVOKE_DEFAULT', message=message)


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
