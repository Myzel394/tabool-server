from datetime import datetime, date, time
from typing import *

from dateutil import parser

StringRepresentationTypes = Union[
    str,
    int,
    float,
    datetime,
    date,
    time,
    None
]
STRING_NULL_VALUES = {"", "null"}


__all__ = [
    "parse"
]


def parse(inp):
    typ = type(inp)
    
    if typ is dict:
        return parse_dict(inp)
    elif typ is list:
        return parse_list(inp)
    elif typ is str:
        return parse_str(inp)
    
    return inp
    

def parse_list(value: list) -> list:
    return [
        parse(element)
        for element in value
    ]


def parse_dict(value: dict) -> dict:
    return {
        key: parse(val)
        for key, val in value.items()
    }


def parse_str(value: str) -> StringRepresentationTypes:
    # Int
    if value.isdigit():
        return int(value)
    # Float
    if value.isdecimal():
        return float(value)
    
    # Datetime
    try:
        parsed = parser.parse(value)
    except ValueError:
        pass
    else:
        return parsed
    
    # None
    if value.lower() in STRING_NULL_VALUES:
        return None
    
    # Normal string
    return value
