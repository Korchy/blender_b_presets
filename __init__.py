# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_b_presets

import bpy
from bpy.app.handlers import persistent
import functools
from .addon import Addon
from . import message_box
from . import render_presets_ops
from . import render_presets_panel
from . import render_presets_preferences
from . import render_presets_presets
from .render_presets import RenderPresets


bl_info = {
    'name': 'b_presets',
    'category': 'All',
    'author': 'Akimov Nikita',
    'version': (1, 1, 8),
    'blender': (2, 83, 0),
    'location': 'N-Panel > B-Presets',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-b-presets/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-b-presets/',
    'description': 'B-Presets'
}


@persistent
def render_presets_load_presets_list(context, scene):
    # load presets list
    if bpy.context:
        RenderPresets.load_presets_list(context=bpy.context)
    else:
        return 0.25


def register():
    if not Addon.dev_mode():
        message_box.register()
        render_presets_preferences.register()
        render_presets_presets.register()
        render_presets_ops.register()
        render_presets_panel.register()
        # load presets list
        bpy.app.timers.register(
            functools.partial(render_presets_load_presets_list, bpy.context, None),
            first_interval=0.25
        )
        # reload presets list with scene load
        if render_presets_load_presets_list not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(render_presets_load_presets_list)
    else:
        print(
            'It seems you are trying to use the dev version of the '
            + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!'
        )


def unregister():
    if not Addon.dev_mode():
        if render_presets_load_presets_list in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(render_presets_load_presets_list)
        RenderPresets.clear_presets_list(context=bpy.context)
        render_presets_panel.unregister()
        render_presets_ops.unregister()
        render_presets_presets.unregister()
        render_presets_preferences.unregister()
        message_box.unregister()


if __name__ == '__main__':
    register()
