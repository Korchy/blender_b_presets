# B-Presets
Blender add-on for saving render and viewport settings to presets and quickly switching between them.

<img src="https://b3d.interplanety.org/wp-content/upload_content/2020/02/preview_670x335-400x200.jpg"><p>

Sometimes it is necessary to have several settings for several final renders, for example, a small preview, a technical render with the metadata output on the image, a "gypsum" render, etc. Each time, manually resizing, changing sampling, marking or unchecking the necessary render settings checkboxes is tedious. The "B-Presets" add-on allows you to save the current render settings into a preset, and then switch between saved presets with a single mouse click. Also, the add-on allows you to save and quickly switch between viewport settings.

Add-on functionality:
-
- Press the “+” button in the add-on panel to create new presets.
- Press the "Save scene to active preset" button to save the current settings to an active template
- To quickly load settings from the preset, just click the button with the monitor image next to the preset name in the list

<img src="https://b3d.interplanety.org/wp-content/upload_content/2020/02/preview_02_670x335-400x200.jpg"><p>

In order to quickly make some renders with different settings, mark the necessary presets checkboxes and press the "Render with marked presets" button. Render results will be saved to the directory specified in the add-on settings.

The add-on allows you to save settings for both rendering and viewport display settings.

To apply the settings preset only for a specific camera, you can specify the desired camera for the preset in a special field.

To protect saved settings from overwriting the preset can be locked for changes by clicking the lock icon.

Settings templates are saved as separate files, making them easy to backup and transfer.

Current add-on version:
-
1.1.8.

Blender versions:
-
2.83, 2.90, 2.91, 2.92, 2.93, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.0, 4.1

Location and call:
-
"3D Viewport" window - N-panel - the "B-Presets" tab

Installation:
-
Download the *.zip archive with the add-on distributive.

The "Preferences" window — Add-ons — Install... — specify the downloaded archive.

Version history:
-
1.1.8.
- updating for Blender 4.1 compatibility    

1.1.7.
- updating for Blender 3.5 compatibility    
- fixing issues with some external add-ons

1.1.6.
- fixing issue with camera settings after ctrl+z

- 1.1.5.
- some fixing in processing Enum attributes

1.1.4.
- some improvements in working with attributes

1.1.3.
- fixed some bugs

1.1.2.
- fixed some bugs

1.1.1.
- presets sorted alphabetically on load

1.1.0.
- 2.82 updated
- excluded the name of the Scene
- added active view_layer settings (optional)
- added saving curves from Color management

1.0.0.
- This release.
