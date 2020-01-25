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
            print(file)

    @classmethod
    def add_new_preset(cls, context):
        # Create new preset
        preset_file_name = cls._get_new_file_name(context=context)
        preset_data = cls._get_preset_data(context=context)
        with open(os.path.join(cls._presets_folder_path(context=context), preset_file_name), 'w') as preset_file:
            json.dump(preset_data, preset_file, indent=4)

    @classmethod
    def _get_preset_data(cls, context):
        # returns preset data
        preset_data = dict()
        # camera
        preset_data['camera_name'] = context.scene.camera.name
        # attributes
        preset_data['attributes'] = dict()
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_x', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_y', context=context, preset_data=preset_data)
        return preset_data

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
