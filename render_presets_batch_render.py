# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import functools
import os
import tempfile
import bpy
# from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, PointerProperty
# from bpy.types import PropertyGroup, WindowManager, Object
# from bpy.utils import register_class, unregister_class
# import re
from bpy.app.handlers import render_complete, render_cancel
from .render_presets import RenderPresets


class BatchRender:

    _presets = None
    _current_preset = None
    _context = None
    _backup = None

    @classmethod
    def batch_render_with_presets(cls, context, presets: list):
        # start butch render with presets by presets_number
        if presets:
            cls._presets = presets
            cls._context = context
            cls._backup = RenderPresets.preset_data_from_scene(context=context)
            cls._render_nex_preset()

    @classmethod
    def _render_nex_preset(cls):
        # render with next preset else clear
        if cls._presets:
            cls._current_preset = cls._presets.pop()
            RenderPresets.preset_to_scene(
                context=cls._context,
                preset=cls._current_preset
            )
            if cls._on_render_finish not in render_complete:
                render_complete.append(cls._on_render_finish)
            if cls._on_render_cancel not in render_cancel:
                render_cancel.append(cls._on_render_cancel)
            # bpy.ops.render.render('INVOKE_DEFAULT')
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
        # on render finish
        cls._save_image(scene=scene)
        # render wit next preset
        cls._render_nex_preset()

    @classmethod
    def _on_render_cancel(cls):
        # on render cancel
        cls.clear()

    @classmethod
    def _save_image(cls, scene):
        # save image from current render
        dest_dir = cls._abs_path(
            path=cls._context.preferences.addons[__package__].preferences.batch_render_output_dir
        )
        if dest_dir:
            if not os.path.isdir(dest_dir):
                os.mkdir(dest_dir)
            file_name = cls._current_preset.name + cls._context.scene.render.file_extension
            file_path = os.path.join(dest_dir, file_name)
            bpy.data.images['Render Result'].save_render(filepath=file_path)
            # for current_area in cls._context.window_manager.windows[0].screen.areas:
            #     if current_area.type == 'IMAGE_EDITOR':
            #         override_area = cls._context.copy()
            #         override_area['area'] = current_area
            #         bpy.ops.image.save_as(override_area, copy=True, filepath=file_path)
            #         break

    @staticmethod
    def _abs_path(path):
        # returns absolute file path from path
        if not path:
            path = tempfile.gettempdir()
        if path[:2] == '//':
            return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), path[2:]))
        else:
            return os.path.abspath(path)

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
