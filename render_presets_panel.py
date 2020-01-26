# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

from bpy.types import Panel, UIList
from bpy.utils import register_class, unregister_class


class RENDER_PRESETS_PT_panel(Panel):
    bl_idname = 'RENDER_PRESETS_PT_panel'
    bl_label = 'Render Presets'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render Presets'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list(
            listtype_name='RENDER_PRESETS_UL_presets_list',
            list_id='rener_presets_list',
            dataptr=context.window_manager,
            propname='render_presets_presets',
            active_dataptr=context.window_manager,
            active_propname='render_presets_active_preset'
        )
        row = layout.row()
        row.operator('render_presets.add_new_preset', icon='PLUS', text='Add new preset')
        row.operator('render_presets.remove_active_preset', icon='CANCEL', text='Remove active preset')
        # row.operator('parametrizer.modify_parameter', icon='MODIFIER_ON', text='Modify active parameter').action = 'SHOW_PANEL'
        # box = layout.box()
        # box.label(text='Options')
        # box.prop(context.preferences.addons[__package__].preferences, 'enable_animation', text='Enable Animation')


class RENDER_PRESETS_UL_presets_list(UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        layout.prop(data=item, property='checked', text='')
        layout.prop(data=item, property='name', text='', emboss=False)
        layout.prop(
            data=item,
            property='locked',
            text='',
            icon='LOCKED' if item.locked else 'UNLOCKED',
            emboss=False
        )


def register():
    register_class(RENDER_PRESETS_UL_presets_list)
    register_class(RENDER_PRESETS_PT_panel)


def unregister():
    unregister_class(RENDER_PRESETS_PT_panel)
    unregister_class(RENDER_PRESETS_UL_presets_list)
