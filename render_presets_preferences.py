# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

from bpy.types import AddonPreferences
from bpy.props import StringProperty
from bpy.utils import register_class, unregister_class


class RENDER_PRESETS_preferences(AddonPreferences):

    bl_idname = __package__

    presets_dir: StringProperty(
        name='Presets directory',
        subtype='DIR_PATH',
        default='//presets/'
    )

    batch_render_output_dir: StringProperty(
        name='Batch render output folder',
        subtype='DIR_PATH',
        default='//presets_output/'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'presets_dir')
        layout.prop(self, 'batch_render_output_dir')


def register():
    register_class(RENDER_PRESETS_preferences)


def unregister():
    unregister_class(RENDER_PRESETS_preferences)
