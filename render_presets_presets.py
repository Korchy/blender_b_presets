# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import bpy
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, WindowManager, Object
from bpy.utils import register_class, unregister_class
import re
from .render_presets import RenderPresets


class RENDER_PRESETS_presets_list(PropertyGroup):

    name: StringProperty(
        update=lambda self, context: self._on_name_update(
            self=self,
            context=context
        )
    )

    name_old: StringProperty(
        default=''
    )

    checked: BoolProperty(
        default=False
    )

    locked: BoolProperty(
        default=False,
        update=lambda self, context: self._on_locked_update(
            self=self,
            context=context
        )
    )

    camera: PointerProperty(
        type=Object,
        poll=lambda self, check_object: self._camera_poll(
            self=self,
            check_object=check_object
        ),
        update=lambda self, context: self._on_camera_update(
            self=self,
            context=context
        )
    )

    camera_old: PointerProperty(
        type=Object
    )

    loaded: BoolProperty(
        default=False
    )

    @staticmethod
    def _on_name_update(self, context):
        # on name changed (already changed)
        if self.loaded and self.name != self.name_old:
            if self.locked:
                self._restore_name(self, message='Can\'t rename locked preset!')
            elif not self.name:
                self._restore_name(self, message='Empty name!')
            elif  re.search('[/\\:\*\?«<>\|%!@+]', self.name):
                self._restore_name(self, message='Unacceptable characters / \\ : * ? « < > | + % @ !')
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

    @staticmethod
    def _camera_poll(self, check_object):
        # filtering only cameras in the drop-down list
        if not self.locked and check_object.type == 'CAMERA':
            return True
        else:
            return False

    @staticmethod
    def _on_camera_update(self, context):
        if self.loaded and self.camera != self.camera_old:
            if self.locked:
                self._restore_camera(self, message='Can\'t change locked preset!')
            else:
                RenderPresets.change_preset_camera(
                    context=context,
                    preset_item=self
                )
        self.camera_old = self.camera

    @staticmethod
    def _restore_camera(self, message=''):
        # restore camera from camera_old with showing warning message
        self.camera = self.camera_old
        bpy.ops.render_presets.messagebox('INVOKE_DEFAULT', message=message)

    @staticmethod
    def _on_locked_update(self, context):
        if self.loaded:
            RenderPresets.change_preset_lock(
                context=context,
                preset=self,
                lock_status=self.locked
            )


def register():
    register_class(RENDER_PRESETS_presets_list)
    WindowManager.render_presets_presets = CollectionProperty(type=RENDER_PRESETS_presets_list)
    WindowManager.render_presets_active_preset = IntProperty(
        name='active preset',
        default=0
    )


def unregister():
    del WindowManager.render_presets_active_preset
    del WindowManager.render_presets_presets
    unregister_class(RENDER_PRESETS_presets_list)
