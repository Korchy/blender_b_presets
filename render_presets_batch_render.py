# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import functools
import os
import bpy
from bpy.app.handlers import render_complete, render_cancel
from .render_presets import RenderPresets
from .render_presets_file_system import RenderPresetsFileSystem

class BatchRender:

    _presets = None
    _current_preset = None
    _context = None
    _backup = None
    _backup_camera = None

    @classmethod
    def batch_render_with_presets(cls, context, presets: list):
        # start batch render with presets
        if presets:
            cls._presets = presets
            cls._context = context
            cls._backup = RenderPresets.preset_data_from_scene(context=context)
            cls._backup_camera = context.scene.camera
            cls._render_nex_preset(context=context)

    @classmethod
    def _render_nex_preset(cls, context):
        # render with next preset else clear
        if cls._presets:
            cls._current_preset = cls._presets.pop()
            context.scene.camera = cls._backup_camera
            RenderPresets.preset_to_scene(
                context=cls._context,
                preset=cls._current_preset
            )
            if cls._on_render_finish not in render_complete:
                render_complete.append(cls._on_render_finish)
            if cls._on_render_cancel not in render_cancel:
                render_cancel.append(cls._on_render_cancel)
            # render with first preset
            bpy.app.timers.register(functools.partial(cls._render), first_interval=1.0)
        else:
            cls.clear()

    @classmethod
    def _render(cls):
        # execute render
        rez = {'CANCELLED'}
        for current_area in cls._context.window_manager.windows[0].screen.areas:
            if current_area.type == 'VIEW_3D':
                override_area = cls._context.copy()
                override_area['area'] = current_area
                override_area['window'] = bpy.context.window_manager.windows[0]
                rez = bpy.ops.render.render(override_area, 'INVOKE_DEFAULT')
                break
        if rez == {'CANCELLED'}:
            # retry with timer
            return 1.0
        else:
            return None

    @classmethod
    def _on_render_finish(cls, scene, unknown):
        # on finish render with current preset
        cls._save_image(scene=scene)
        # render wit next preset
        cls._render_nex_preset(context=cls._context)

    @classmethod
    def _on_render_cancel(cls):
        # on render cancel
        cls.clear()

    @classmethod
    def _save_image(cls, scene):
        # save image from current render
        dest_dir = RenderPresetsFileSystem.abs_path(
            path=cls._context.preferences.addons[__package__].preferences.batch_render_output_dir
        )
        if dest_dir:
            if not os.path.isdir(dest_dir):
                os.mkdir(dest_dir)
            # file_name = cls._current_preset.name + cls._context.scene.render.file_extension
            file_name = cls._current_preset.name + scene.render.file_extension
            file_path = os.path.join(dest_dir, file_name)
            bpy.data.images['Render Result'].save_render(filepath=file_path)

    @classmethod
    def clear(cls):
        cls._presets = None
        cls._current_preset = None
        RenderPresets.preset_data_to_scene(
            context=cls._context,
            preset_data=cls._backup
        )
        cls._context = None
        cls._backup = None
        if cls._on_render_finish in render_complete:
            render_complete.remove(cls._on_render_finish)
        if cls._on_render_cancel in render_cancel:
            render_cancel.remove(cls._on_render_cancel)
