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
        default='i:/dev/python/blender/blender_render_presets/presets/'     # ToDo remove
    )

    def draw(self, context):
        self.layout.prop(self, 'presets_dir')


def register():
    register_class(RENDER_PRESETS_preferences)


def unregister():
    unregister_class(RENDER_PRESETS_preferences)
