# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import json
import os
from mathutils import Vector, Color
from bpy.types import bpy_prop_array
from .render_presets_file_system import RenderPresetsFileSystem


class RenderPresets:

    _presets_folder = 'presets'
    _preset_file_name = 'preset'
    _preset_file_ext = 'json'
    _scene_backup = None
    _camera_backup = None

    @classmethod
    def load_presets_list(cls, context):
        # load presets list
        # clear current
        cls.clear_presets_list(context=context)
        # load new from files
        for file in cls._presets_files(context=context):
            preset = context.window_manager.render_presets_presets.add()
            preset.name = os.path.splitext(file)[0]
            preset_data = cls._preset_data_from_file(
                context=context,
                preset_file_name=file
            )
            if preset_data:
                preset.locked = preset_data['locked']
                preset.camera = cls._object_by_name(
                    context=context,
                    object_name=preset_data['camera_name']
                )
                preset.loaded = True

    @classmethod
    def add_new_preset(cls, context):
        # Create new preset
        preset_file_name = cls._get_new_file_name(context=context)
        preset_data = cls.preset_data_from_scene(context=context)
        cls._preset_data_to_file(
            context=context,
            preset_file_name=preset_file_name,
            preset_data=preset_data
        )
        # add to list
        new_preset = context.window_manager.render_presets_presets.add()
        new_preset.name = os.path.splitext(preset_file_name)[0]
        new_preset.loaded = True

    @classmethod
    def remove_preset(cls, context, preset):
        # Remove active preset
        if not preset.locked:
            # remove file
            file_path = os.path.join(cls._presets_folder_path(context=context), preset.name + '.' + cls._preset_file_ext)
            if os.path.isfile(path=file_path):
                os.remove(path=file_path)
            # remove item in list
            context.window_manager.render_presets_presets.remove(context.window_manager.render_presets_active_preset)

    @classmethod
    def scene_to_preset(cls, context, preset):
        # Store scene settings to active preset file
        if not preset.locked:
            preset_data = cls.preset_data_from_scene(context=context)
            preset_data['camera_name'] = preset.camera.name if preset.camera else ''
            cls._preset_data_to_file(
                context=context,
                preset_file_name=preset.name + '.' + cls._preset_file_ext,
                preset_data=preset_data
            )

    @classmethod
    def preset_to_scene(cls, context, preset):
        # Load scene settings from active preset
        cls.preset_data_to_scene(
            context=context,
            preset_data=cls._preset_data_from_file(
                context=context,
                preset_file_name=preset.name + '.' + cls._preset_file_ext
            )
        )

    @classmethod
    def preset_data_from_scene(cls, context):
        # returns preset data
        preset_data = dict()
        # lock
        preset_data['locked'] = False
        # camera
        preset_data['camera_name'] = ''
        # attributes
        preset_data['attributes'] = dict()
        # add here data to save to the preset
        # render
        # context.scene
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene,
            render_property_txt='context.scene',
            excluded_attributes=(
                'rna_type', 'active_clip', 'animation_data', 'background_set', 'camera', 'collection', 'cursor', 'cycles', 'cycles_curves',
                'display', 'display_settings', 'eevee', 'frame_current_final', 'grease_pencil', 'is_evaluated', 'is_library_indirect',
                'is_nla_tweakmode', 'keying_sets', 'keying_sets_all', 'library', 'name_full', 'node_tree', 'objects', 'original',
                'override_library', 'preview', 'render', 'rigidbody_world', 'safe_areas', 'sequence_editor', 'sequencer_colorspace_settings',
                'timeline_markers', 'tool_settings', 'transform_orientation_slots', 'unit_settings', 'users', 'view_layers', 'view_settings',
                'world'
            ),
            preset_data=preset_data
        )
        # context.scene.render
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render,
            render_property_txt='context.scene.render',
            excluded_attributes=(
                'rna_type', 'bake', 'ffmpeg', 'file_extension', 'has_multiple_engines', 'image_settings', 'is_movie_format',
                'motion_blur_shutter_curve', 'stereo_views', 'use_spherical_stereo', 'views'
            ),
            preset_data=preset_data
        )
        # context.scene.render.bake
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.bake,
            render_property_txt='context.scene.render.bake',
            excluded_attributes=(
                'rna_type', 'cage_object', 'image_settings', 'pass_filter'
            ),
            preset_data=preset_data
        )
        # context.scene.render.ffmpeg
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.ffmpeg,
            render_property_txt='context.scene.render.ffmpeg',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.render.image_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.image_settings,
            render_property_txt='context.scene.render.image_settings',
            excluded_attributes=(
                'rna_type', 'display_settings', 'stereo_3d_format', 'view_settings'
            ),
            preset_data=preset_data
        )
        # context.scene.render.image_settings.view_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.image_settings.view_settings,
            render_property_txt='context.scene.render.image_settings.view_settings',
            excluded_attributes=(
                'rna_type', 'curve_mapping'
            ),
            preset_data=preset_data
        )
        # context.scene.render.image_settings.display_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.image_settings.display_settings,
            render_property_txt='context.scene.render.image_settings.display_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.render.bake.image_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.bake.image_settings,
            render_property_txt='context.scene.render.bake.image_settings',
            excluded_attributes=(
                'rna_type', 'display_settings', 'stereo_3d_format', 'view_settings'
            ),
            preset_data=preset_data
        )
        # context.scene.render.bake.image_settings.view_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.bake.image_settings.view_settings,
            render_property_txt='context.scene.render.bake.image_settings.view_settings',
            excluded_attributes=(
                'rna_type', 'curve_mapping'
            ),
            preset_data=preset_data
        )
        # context.scene.render.bake.image_settings.display_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.render.bake.image_settings.display_settings,
            render_property_txt='context.scene.render.bake.image_settings.display_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.view_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.view_settings,
            render_property_txt='context.scene.view_settings',
            excluded_attributes=(
                'rna_type', 'curve_mapping'
            ),
            preset_data=preset_data
        )
        # context.scene.cycles
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.cycles,
            render_property_txt='context.scene.cycles',
            excluded_attributes=(
                'rna_type', 'dicing_camera'
            ),
            preset_data=preset_data
        )
        # context.scene.cycles_curves
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.cycles_curves,
            render_property_txt='context.scene.cycles_curves',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.display
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.display,
            render_property_txt='context.scene.display',
            excluded_attributes=(
                'rna_type', 'shading'
            ),
            preset_data=preset_data
        )
        # context.scene.display.shading
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.display.shading,
            render_property_txt='context.scene.display.shading',
            excluded_attributes=(
                'rna_type', 'cycles', 'selected_studio_light'
            ),
            preset_data=preset_data
        )
        # context.scene.display_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.display_settings,
            render_property_txt='context.scene.display_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.eevee
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.eevee,
            render_property_txt='context.scene.eevee',
            excluded_attributes=(
                'rna_type', 'gi_cache_info'
            ),
            preset_data=preset_data
        )
        # context.scene.sequencer_colorspace_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.sequencer_colorspace_settings,
            render_property_txt='context.scene.sequencer_colorspace_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.unit_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.unit_settings,
            render_property_txt='context.scene.unit_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.world
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.world,
            render_property_txt='context.scene.world',
            excluded_attributes=(
                'rna_type', 'animation_data', 'cycles', 'cycles_visibility', 'is_evaluated', 'is_library_indirect', 'library', 'light_settings',
                'mist_settings', 'name_full', 'node_tree', 'original', 'override_library', 'preview', 'users'
            ),
            preset_data=preset_data
        )
        # context.scene.world.cycles
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.world.cycles,
            render_property_txt='context.scene.world.cycles',
            excluded_attributes=(
                'rna_type', 'animation_data', 'cycles'
            ),
            preset_data=preset_data
        )
        # context.scene.world.cycles_visibility
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.world.cycles_visibility,
            render_property_txt='context.scene.world.cycles_visibility',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.world.light_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.world.light_settings,
            render_property_txt='context.scene.world.light_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # context.scene.world.mist_settings
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.scene.world.mist_settings,
            render_property_txt='context.scene.world.mist_settings',
            excluded_attributes=(
                'rna_type'
            ),
            preset_data=preset_data
        )
        # viewport
        # context.space_data
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.space_data,
            render_property_txt='context.space_data',
            excluded_attributes=(
                'rna_type', 'camera', 'icon_from_show_object_viewport', 'local_view', 'lock_object', 'overlay', 'region_3d', 'region_quadviews',
                'shading', 'show_region_ui', 'stereo_3d_eye', 'type'
            ),
            preset_data=preset_data
        )
        # context.space_data.overlay
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.space_data.overlay,
            render_property_txt='context.space_data.overlay',
            excluded_attributes=(
                'rna_type', 'grid_scale_unit'
            ),
            preset_data=preset_data
        )
        # context.space_data.shading
        cls._add_attributes_to_preset_data(
            context=context,
            render_property=context.space_data.shading,
            render_property_txt='context.space_data.shading',
            excluded_attributes=(
                'rna_type', 'cycles', 'selected_studio_light'
            ),
            preset_data=preset_data
        )
        return preset_data

    @classmethod
    def _add_attributes_to_preset_data(cls, context, render_property, render_property_txt, excluded_attributes, preset_data):
        # add render property attributes to preset data
        attributes = (attribute for attribute in dir(render_property) if
                      not attribute.startswith('__')
                      and not attribute.startswith('bl_')
                      and attribute not in excluded_attributes
                      and hasattr(render_property, attribute)
                      and not callable(getattr(render_property, attribute))
                      )
        for attribute in attributes:
            if render_property.is_property_readonly(attribute):
                print(attribute, ' (', type(getattr(render_property, attribute)), ') ', ': ', getattr(render_property, attribute), 'READ_ONLY')
            elif isinstance(getattr(render_property, attribute), bpy_prop_array):
                cls._add_attribute_to_preset_data(attribute=render_property_txt + '.' + attribute, context=context, preset_data=preset_data, attribute_type='bpy_prop_array')
            elif isinstance(getattr(render_property, attribute), (Vector, Color)):
                cls._add_attribute_to_preset_data(attribute=render_property_txt + '.' + attribute, context=context, preset_data=preset_data, attribute_type='Vector')
            elif not isinstance(getattr(render_property, attribute), (int, float, bool, str, set)):
                print(attribute, ' (', type(getattr(render_property, attribute)), ') ', ': ', getattr(render_property, attribute), 'COMPLEX TYPE')
            else:
                cls._add_attribute_to_preset_data(attribute=render_property_txt + '.' + attribute, context=context, preset_data=preset_data)

    @classmethod
    def preset_data_to_scene(cls, context, preset_data: dict):
        # store preset data to scene properties
        cls._backup_scene(context=context)
        # camera
        if preset_data['camera_name']\
                and preset_data['camera_name'] in context.scene.objects\
                and context.scene.objects[preset_data['camera_name']].type == 'CAMERA':
            context.scene.camera = cls._object_by_name(
                context=context,
                object_name=preset_data['camera_name']
            )
        else:
            context.scene.camera = cls._camera_backup
        # attributes
        for attribute in preset_data['attributes']:
            cls._set_attribute_from_preset_data(
                context=context,
                attribute_text=attribute,
                attribute=preset_data['attributes'][attribute]
            )
        return preset_data

    @classmethod
    def _preset_data_from_file(cls, context, preset_file_name):
        # return preset data from file (saved preset)
        preset_data = None
        file_path = os.path.join(cls._presets_folder_path(context=context), preset_file_name)
        if os.path.isfile(file_path):
            with open(file=file_path, mode='r', encoding='utf8') as preset_file:
                preset_data = json.load(preset_file)
        return preset_data

    @classmethod
    def _preset_data_to_file(cls, context, preset_file_name, preset_data):
        # save preset data to preset file
        file_path = os.path.join(cls._presets_folder_path(context=context), preset_file_name)
        with open(file=file_path, mode='w', encoding='utf8') as preset_file:
            json.dump(preset_data, preset_file, indent=4, ensure_ascii=False)

    @classmethod
    def _backup_scene(cls, context):
        # backup current preset data
        if not cls._scene_backup:
            cls._scene_backup = cls.preset_data_from_scene(context=context)
            cls._camera_backup = context.scene.camera

    @classmethod
    def restore_scene(cls, context):
        # restore scene from backup
        if cls._scene_backup:
            cls.preset_data_to_scene(
                context=context,
                preset_data=cls._scene_backup
            )
            context.scene.camera = cls._camera_backup

    @classmethod
    def clear_presets_list(cls, context):
        # remove all presets from the list
        while context.window_manager.render_presets_presets:
            context.window_manager.render_presets_presets.remove(0)

    @classmethod
    def _add_attribute_to_preset_data(cls, context, preset_data: dict, attribute: str, attribute_type: str = 'prop'):
        # add attribute data to preset dict
        # context needed to eval
        attribute_instance, attribute_name = attribute.rsplit('.', maxsplit=1)
        if hasattr(eval(attribute_instance), attribute_name):
            if attribute_type == 'bpy_prop_array':
                attribute_value = []
                for value in getattr(eval(attribute_instance), attribute_name):
                    attribute_value.append(value)
            elif attribute_type == 'Vector':
                attribute_value = tuple(getattr(eval(attribute_instance), attribute_name))
            else:
                attribute_value = getattr(eval(attribute_instance), attribute_name)
            preset_data['attributes'][attribute] = attribute_value

    @classmethod
    def _set_attribute_from_preset_data(cls, context, attribute_text, attribute):
        # add attribute data to preset dict
        # context needed to eval
        attribute_instance, attribute_name = attribute_text.rsplit('.', maxsplit=1)
        try:
            attribute_instance = eval(attribute_instance)
            if attribute_instance and hasattr(attribute_instance, attribute_name):
                setattr(attribute_instance, attribute_name, attribute)
        except Exception as exception:
            pass

    @classmethod
    def change_preset_name(cls, context, preset_item):
        # changes preset name
        old_file_path = os.path.join(cls._presets_folder_path(context=context), preset_item.name_old + '.' + cls._preset_file_ext)
        if os.path.isfile(old_file_path):
            new_file_path = os.path.join(cls._presets_folder_path(context=context), preset_item.name + '.' + cls._preset_file_ext)
            os.rename(old_file_path, new_file_path)

    @classmethod
    def change_preset_camera(cls, context, preset_item):
        # changes preset camera
        if not preset_item.locked:
            preset_data = cls._preset_data_from_file(
                context=context,
                preset_file_name=preset_item.name + '.' + cls._preset_file_ext
            )
            if preset_data:
                preset_data['camera_name'] = preset_item.camera.name if preset_item.camera else ''
                cls._preset_data_to_file(
                    context=context,
                    preset_file_name=preset_item.name + '.' + cls._preset_file_ext,
                    preset_data=preset_data
                )

    @classmethod
    def change_preset_lock(cls, context, preset, lock_status):
        # changes preset lock status in its file
        preset_data = cls._preset_data_from_file(
            context=context,
            preset_file_name=preset.name + '.' + cls._preset_file_ext
        )
        if preset_data:
            preset_data['locked'] = lock_status
            cls._preset_data_to_file(
                context=context,
                preset_file_name=preset.name + '.' + cls._preset_file_ext,
                preset_data=preset_data
            )

    @classmethod
    def _object_by_name(cls, context, object_name):
        # return object from scene by its name
        obj = None
        if object_name and object_name in context.scene.objects:
            obj = context.scene.objects[object_name]
        return obj

    @classmethod
    def _get_new_file_name(cls, context):
        # Returns unic file name for preset
        uid_postfix = 1
        unic_file_name = cls._preset_file_name + '.' + str(uid_postfix).zfill(3) + '.' + cls._preset_file_ext
        while unic_file_name in cls._presets_files(context=context):
            uid_postfix += 1
            unic_file_name = cls._preset_file_name + '.' + str(uid_postfix).zfill(3) + '.' + cls._preset_file_ext
        return unic_file_name

    @classmethod
    def _presets_files(cls, context):
        # generator to get preset files in presets folder
        for file in os.listdir(cls._presets_folder_path(context=context)):
            if os.path.isfile(os.path.join(cls._presets_folder_path(context=context), file)) and file.endswith('.' + cls._preset_file_ext):
                yield file

    @classmethod
    def _presets_folder_path(cls, context):
        # Return full path to presets folder
        presets_dir = None
        if context.preferences.addons[__package__].preferences.presets_dir:
            presets_dir = RenderPresetsFileSystem.abs_path(
                path=context.preferences.addons[__package__].preferences.presets_dir
            )
        else:
            presets_dir = os.path.join(os.path.dirname(__file__), cls._presets_folder)
        if presets_dir:
            if not os.path.isdir(presets_dir):
                os.mkdir(presets_dir)
        return presets_dir
