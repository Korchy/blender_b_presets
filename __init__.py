# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

from .addon import Addon
from . import message_box
from . import render_presets_ops
from . import render_presets_panel
from . import render_presets_preferences
from . import render_presets_presets


bl_info = {
    'name': 'render_presets',
    'category': 'All',
    'author': 'Akimov Nikita',
    'version': (1, 0, 0),
    'blender': (2, 81, 0),
    'location': 'N-Panel > Render Presets',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-render-presets/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-render-presets/',
    'description': 'Render Presets'
}


def register():
    if not Addon.dev_mode():
        message_box.register()
        render_presets_preferences.register()
        render_presets_presets.register()
        render_presets_ops.register()
        render_presets_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        render_presets_panel.unregister()
        render_presets_ops.unregister()
        render_presets_presets.unregister()
        render_presets_preferences.unregister()
        message_box.unregister()


if __name__ == '__main__':
    register()
