import re

__all__ = [
    "camel_to_snake", "max_length_from_choices"
]


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def max_length_from_choices(choices: list[tuple[str, str]]) -> int:
    all_lengths = [
        len(db_value)
        for db_value, _ in choices
    ]
    
    return max(*all_lengths)
