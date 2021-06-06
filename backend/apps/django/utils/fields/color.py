from typing import *

from colour import Color
from django.db import models
from django.utils.translation import gettext as _

__all__ = [
    "ColorField", "RGBTupleType"
]

RGB_JOIN_CHARACTER = ","
RGBTupleType = Tuple[float, float, float]


def rgb_tuple_to_string(rgb: RGBTupleType, join: str = RGB_JOIN_CHARACTER) -> str:
    red = int(rgb[0] * 255)
    green = int(rgb[1] * 255)
    blue = int(rgb[2] * 255)

    return join.join([str(red), str(green), str(blue)])


def string_to_rgb_tuple(rgb: str, join: str = RGB_JOIN_CHARACTER) -> RGBTupleType:
    # noinspection PyTypeChecker
    return tuple([
        float(element) / 255
        for element in rgb.split(join)
    ])


def parse_string(value: str) -> Color:
    return Color(rgb=string_to_rgb_tuple(value))


class ColorField(models.CharField):
    description = _("Feld für Farbe")

    __defaults = {
        "max_length": len(
            rgb_tuple_to_string([1, 1, 1])
        )
    }

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = kwargs.get("max_length") or self.__defaults["max_length"]

        super().__init__(*args, **kwargs)

    def value_to_string(self, obj):
        obj = super().value_to_string(obj)

        return f"rgb({rgb_tuple_to_string(obj)})"

    def get_db_prep_save(self, value, connection):
        # Field will be saved to database
        if value is None:
            value = None
        else:
            value = rgb_tuple_to_string(Color(value).rgb)

        return super().get_db_prep_save(value, connection)

    def from_db_value(self, value, expression, connection) -> Optional[Color]:  # skipcq: PYL-W0613
        # Field is accessed in Python
        if value is None:
            return None
        if isinstance(value, Color):
            return value

        return Color(rgb=string_to_rgb_tuple(value))

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        # Iterate custom parameters
        for field, default in self.__defaults.items():
            # Only add, if it's not the default value
            if (value := getattr(self, field)) != default:
                kwargs[field] = value

        return name, path, args, kwargs
