# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_b_presets

from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty
from bpy.utils import register_class, unregister_class


class RENDER_PRESETS_preferences(AddonPreferences):

    bl_idname = __package__

    presets_dir: StringProperty(
        name='Presets directory',
        subtype='DIR_PATH',
        default=''
    )

    batch_render_output_dir: StringProperty(
        name='Batch render output folder',
        subtype='DIR_PATH',
        default='//presets_output/'
    )

    use_active_view_layer: BoolProperty(
        default=True,
        name='Save active view layer settings'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'presets_dir')
        layout.prop(self, 'batch_render_output_dir')
        layout.label(text='Addition properties:')
        row = layout.row()
        row.prop(self, 'use_active_view_layer', toggle=True)


def register():
    register_class(RENDER_PRESETS_preferences)


def unregister():
    unregister_class(RENDER_PRESETS_preferences)
