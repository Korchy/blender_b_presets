# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import json
import os


class RenderPresets:

    _presets_folder = 'presets'
    _preset_file_name = 'preset'
    _preset_file_ext = 'json'

    @classmethod
    def load_presets_list(cls, context):
        # load presets list
        for file in cls._presets_files(context=context):
            new_preset = context.window_manager.render_presets_presets.add()
            new_preset.name = os.path.splitext(file)[0]
            preset_data = cls._preset_data_from_file(
                context=context,
                preset_file_name=file
            )
            if preset_data:
                new_preset.locked = preset_data['locked']

    @classmethod
    def add_new_preset(cls, context):
        # Create new preset
        preset_file_name = cls._get_new_file_name(context=context)
        preset_data = cls._preset_data_from_scene(context=context)
        cls._preset_data_to_file(
            context=context,
            preset_file_name=preset_file_name,
            preset_data=preset_data
        )
        # add to list
        new_preset = context.window_manager.render_presets_presets.add()
        new_preset.name = os.path.splitext(preset_file_name)[0]

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
    def _preset_data_from_scene(cls, context):
        # returns preset data
        preset_data = dict()
        # lock
        preset_data['locked'] = False
        # camera
        preset_data['camera_name'] = context.scene.camera.name
        # attributes
        preset_data['attributes'] = dict()
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_x', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_y', context=context, preset_data=preset_data)
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
    def clear_presets_list(cls, context):
        # remove all presets from the list
        while context.window_manager.render_presets_presets:
            context.window_manager.render_presets_presets.remove(0)

    @classmethod
    def _add_attribute_to_preset_data(cls, context, preset_data: dict, attribute: str):
        # add attribute data to preset dict
        attribute_instance, attribute_name = attribute.rsplit('.', maxsplit=1)
        preset_data['attributes'][attribute] = {
            'instance': attribute_instance,
            'attribute': attribute_name,
            'value': getattr(eval(attribute_instance), attribute_name)
        }

    @classmethod
    def change_preset_name(cls, context, preset_item):
        # changes preset name
        old_file_path = os.path.join(cls._presets_folder_path(context=context), preset_item.name_old + '.' + cls._preset_file_ext)
        if os.path.isfile(old_file_path):
            new_file_path = os.path.join(cls._presets_folder_path(context=context), preset_item.name + '.' + cls._preset_file_ext)
            os.rename(old_file_path, new_file_path)

    @classmethod
    def change_preset_lock(cls, context, preset_name, lock_status):
        # changes preset lock status in its file
        preset_data = cls._preset_data_from_file(
            context=context,
            preset_file_name=preset_name + '.' + cls._preset_file_ext
        )
        if preset_data:
            preset_data['locked'] = lock_status
            cls._preset_data_to_file(
                context=context,
                preset_file_name=preset_name + '.' + cls._preset_file_ext,
                preset_data=preset_data
            )

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
            presets_dir = context.preferences.addons[__package__].preferences.presets_dir
        else:
            presets_dir = os.path.join(os.path.dirname(__file__), cls._presets_folder)
        if presets_dir:
            if not os.path.isdir(presets_dir):
                os.mkdir(presets_dir)
        return presets_dir
