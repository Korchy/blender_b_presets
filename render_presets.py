# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_render_presets

import json
import os
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
            cls._preset_data_to_file(
                context=context,
                preset_file_name=preset.name + '.' + cls._preset_file_ext,
                preset_data=preset_data
            )
            preset.camera = None

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
        # add here data to save to preset
        # render properties
        cls._add_attribute_to_preset_data(attribute='context.scene.render.engine', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.feature_set', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.device', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.shading_system', context=context, preset_data=preset_data)
        # render properties - sampling
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.progressive', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.samples', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.preview_samples', context=context, preset_data=preset_data)
        # render properties - sampling - advanced
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.seed', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.sampling_pattern', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.use_square_samples', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.min_light_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.min_transparent_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.light_sampling_threshold', context=context, preset_data=preset_data)
        # render properties - light path - max bounces
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.max_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.diffuse_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.glossy_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.transparent_max_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.transmission_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.volume_bounces', context=context, preset_data=preset_data)
        # render properties - light path - clamping
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.sample_clamp_direct', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.sample_clamp_indirect', context=context, preset_data=preset_data)
        # render properties - light path - caustics
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.blur_glossy', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.caustics_reflective', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.caustics_refractive', context=context, preset_data=preset_data)
        # render properties - volume
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.volume_step_size', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.volume_max_steps', context=context, preset_data=preset_data)
        # render properties - hair
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles_curves.use_curves', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles_curves.shape', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles_curves.cull_backfacing', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles_curves.primitive', context=context, preset_data=preset_data)
        # render properties - simplify - viewport
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_simplify', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_subdivision', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_child_particles', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.texture_limit', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.ao_bounces', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_simplify_smoke_highres', context=context, preset_data=preset_data)
        # render properties - simplify - render
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_subdivision_render', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_child_particles_render', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.texture_limit_render', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.ao_bounces_render', context=context, preset_data=preset_data)
        # render properties - simplify - culling
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.use_camera_cull', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.camera_cull_margin', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.use_distance_cull', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.distance_cull_margin', context=context, preset_data=preset_data)
        # render properties - simplify - grease pencil
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_onplay', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_view_modifier', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_shader_fx', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_blend', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_tint', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_view_fill', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.simplify_gpencil_remove_lines', context=context, preset_data=preset_data)
        # render properties - motion blur
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_motion_blur', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.motion_blur_position', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.motion_blur_shutter', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.rolling_shutter_type', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.rolling_shutter_duration', context=context, preset_data=preset_data)
        # render properties - film
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.film_exposure', context=context, preset_data=preset_data)
        # render properties - film - pixel filter
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.pixel_filter_type', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.filter_width', context=context, preset_data=preset_data)
        # render properties - film - transparent
        cls._add_attribute_to_preset_data(attribute='context.scene.render.film_transparent', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.film_transparent_glass', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.film_transparent_roughness', context=context, preset_data=preset_data)
        # render properties - performance - threads
        cls._add_attribute_to_preset_data(attribute='context.scene.render.threads_mode', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.threads', context=context, preset_data=preset_data)
        # render properties - performance - tiles
        cls._add_attribute_to_preset_data(attribute='context.scene.render.tile_x', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.tile_y', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.tile_order', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.use_progressive_refine', context=context, preset_data=preset_data)
        # render properties - performance - acceleration structure
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.debug_use_spatial_splits', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.debug_use_hair_bvh', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.debug_bvh_time_steps', context=context, preset_data=preset_data)
        # render properties - performance - final render
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_save_buffers', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_persistent_data', context=context, preset_data=preset_data)
        # render properties - performance - viewport
        cls._add_attribute_to_preset_data(attribute='context.scene.render.preview_pixel_size', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.preview_start_resolution', context=context, preset_data=preset_data)
        # render properties - bake
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_bake_multires', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.cycles.bake_type', context=context, preset_data=preset_data)
        # render properties - bake - influence
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_direct', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_indirect', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_diffuse', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_glossy', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_transmission', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_subsurface', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_ambient_occlusion', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_pass_emit', context=context, preset_data=preset_data)
        # render properties - bake - selected to active
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_selected_to_active', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_cage', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.cage_extrusion', context=context, preset_data=preset_data)
        # render properties - bake - output
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.margin', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.bake.use_clear', context=context, preset_data=preset_data)
        # render properties - freestyle
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_freestyle', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.line_thickness_mode', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.line_thickness', context=context, preset_data=preset_data)
        # render properties - color management
        cls._add_attribute_to_preset_data(attribute='context.scene.display_settings.display_device', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.view_settings.view_transform', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.view_settings.look', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.view_settings.exposure', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.view_settings.gamma', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.sequencer_colorspace_settings.name', context=context, preset_data=preset_data)
        # render properties - color management - use curves
        cls._add_attribute_to_preset_data(attribute='context.scene.view_settings.use_curve_mapping', context=context, preset_data=preset_data)
        # output properties - dimensions
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_x', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_y', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.resolution_percentage', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.pixel_aspect_x', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.pixel_aspect_y', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_border', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_crop_to_border', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.frame_start', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.frame_end', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.frame_step', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.fps', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.fps_base', context=context, preset_data=preset_data)
        # output properties - dimensions - time remapping
        cls._add_attribute_to_preset_data(attribute='context.scene.render.frame_map_old', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.frame_map_new', context=context, preset_data=preset_data)
        # output properties - stereoscopy
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_multiview', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.views_format', context=context, preset_data=preset_data)
        # output properties - output
        cls._add_attribute_to_preset_data(attribute='context.scene.render.filepath', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_overwrite', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_file_extension', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_placeholder', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_render_cache', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.file_format', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.color_mode', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.color_depth', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.compression', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.quality', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.jpeg2k_codec', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.use_jpeg2k_cinema_preset', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.use_jpeg2k_cinema_48', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.use_jpeg2k_ycc', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.use_cineon_log', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.exr_codec', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.use_preview', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.use_zbuffer', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.image_settings.tiff_codec', context=context, preset_data=preset_data)
        # output properties - output - ffmpeg
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.format', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.audio_bitrate', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.audio_channels', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.audio_codec', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.audio_mixrate', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.audio_volume', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.buffersize', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.codec', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.constant_rate_factor', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.ffmpeg_preset', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.format', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.gopsize', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.max_b_frames', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.maxrate', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.minrate', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.muxrate', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.packetsize', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.use_autosplit', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.use_lossless_output', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.use_max_b_frames', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.ffmpeg.video_bitrate', context=context, preset_data=preset_data)
        # output properties - metadata
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_date', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_time', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_render_time', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_frame', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_frame_range', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_memory', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_hostname', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_camera', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_lens', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_scene', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_marker', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_filename', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_sequencer_strip', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_strip_meta', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp_note', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.stamp_note_text', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.use_stamp', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.stamp_font_size', context=context, preset_data=preset_data)
        cls._add_attribute_to_preset_data(attribute='context.scene.render.stamp_foreground', context=context, preset_data=preset_data, attribute_type='bpy_prop_array')


        # viewport
        cls._add_attribute_to_preset_data(attribute='context.space_data.shading.type', context=context, preset_data=preset_data)

        return preset_data

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
            else:
                attribute_value = getattr(eval(attribute_instance), attribute_name)
            preset_data['attributes'][attribute] = {
                'value': attribute_value
            }

    @classmethod
    def _set_attribute_from_preset_data(cls, context, attribute_text, attribute):
        # add attribute data to preset dict
        # context needed to eval
        attribute_instance, attribute_name = attribute_text.rsplit('.', maxsplit=1)
        if hasattr(eval(attribute_instance), attribute_name):
            setattr(eval(attribute_instance), attribute_name, attribute['value'])

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
