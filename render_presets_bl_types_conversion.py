# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender_b_presets

# Blender types to/from JSON conversion
# Blender types with prefix BL

from typing import Dict, Any


class BLBaseType:

    @classmethod
    def to_json(cls, instance) -> Dict[str, Any]:
        # instance to json call
        instance_in_json = {
            'class': type(instance).__name__,
            'instance': cls._instance_to_json(instance=instance)
        }
        return instance_in_json

    @classmethod
    def from_json(cls, instance, json):
        # instance from json call
        return cls._json_to_instance(instance=instance, json=json['instance'])

    @classmethod
    def _instance_to_json(cls, instance):
        # get data from instance and convert them to json
        json = {}
        return json

    @classmethod
    def _json_to_instance(cls, instance, json):
        # get data from json and fill instance with that data
        return instance


class BLColor(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {
            'r': instance.r,
            'g': instance.g,
            'b': instance.b
        }
        return json

    @classmethod
    def _json_to_instance(cls, instance, json):
        # data from json
        instance.r = json['r']
        instance.g = json['g']
        instance.b = json['b']
        return instance


class BLVector(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {
            'x': instance.x,
            'y': instance.y
        }
        if hasattr(instance, 'z'):
            json['z'] = instance.z
        return json

    @classmethod
    def _json_to_instance(cls, instance, json):
        # data from json
        instance.x = json['x']
        instance.y = json['y']
        if hasattr(instance, 'z'):
            instance.z = json['z']
        return instance


class BLSet(BLBaseType):
    # set as separate type because json doesn't serialize "set" type

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = list(instance)
        return json

    @classmethod
    def _json_to_instance(cls, instance, json):
        # data from json
        instance = set(json)
        return instance


class BLCurveMapping(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        json = {
            'use_clip': instance.use_clip,
            'clip_min_x': instance.clip_min_x,
            'clip_min_y': instance.clip_min_y,
            'clip_max_x': instance.clip_max_x,
            'clip_max_y': instance.clip_max_y,
            'black_level': BLColor.to_json(instance.black_level),
            'white_level': BLColor.to_json(instance.white_level),
            'curves': []
        }
        if hasattr(instance, 'extend'):
            json['extend'] = instance.extend
        if hasattr(instance, 'tone'):
            json['tone'] = instance.tone
        for curve_map in instance.curves:
            json['curves'].append(BLCurveMap.to_json(curve_map))
        return json

    @classmethod
    def _json_to_instance(cls, instance, json):
        instance.use_clip = json['use_clip']
        instance.clip_min_x = json['clip_min_x']
        instance.clip_min_y = json['clip_min_y']
        instance.clip_max_x = json['clip_max_x']
        instance.clip_max_y = json['clip_max_y']
        if 'black_level' in json and hasattr(instance, 'black_level'):
            BLColor.from_json(instance.black_level, json['black_level'])
        if 'white_level' in json and hasattr(instance, 'white_level'):
            BLColor.from_json(instance.white_level, json['white_level'])
        if 'extend' in json and hasattr(instance, 'extend'):
            instance.extend = json['extend']
        if 'tone' in json and hasattr(instance, 'tone'):
            instance.tone = json['tone']
        for i, curve in enumerate(json['curves']):
            BLCurveMap.from_json(instance.curves[i], curve)
        instance.update()


class BLCurveMap(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        json = {
            'points': []
        }
        if hasattr(instance, 'extend'):
            json['extend'] = instance.extend
        for point in instance.points:
            json['points'].append(BLCurveMapPoint.to_json(point))
        return json

    @classmethod
    def _json_to_instance(cls, instance, json):
        if 'extend' in json and hasattr(instance, 'extend'):
            instance.extend = json['extend']
        for i, point in enumerate(json['points']):
            if len(instance.points) <= i:
                if 'instance' in point:
                    instance.points.new(
                        point['instance']['location']['instance']['x'], point['instance']['location']['instance']['y']
                    )
                else:   # older compatibility (was [...] now {class: xx, instance={...}})
                    instance.points.new(point['location'][0], point['location'][0])
            BLCurveMapPoint.from_json(instance.points[i], point)


class BLCurveMapPoint(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        return {
            'location': BLVector.to_json(instance=instance.location),
            'handle_type': instance.handle_type,
            'select': instance.select
        }

    @classmethod
    def _json_to_instance(cls, instance, json):
        BLVector.from_json(instance=instance.location, json=json['location'])
        instance.handle_type = json['handle_type']
        instance.select = json['select']
