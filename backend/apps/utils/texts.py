__all__ = [
    "max_length_from_choices"
]


def max_length_from_choices(choices: list[tuple[str, str]]) -> int:
    all_lengths = [
        len(db_value)
        for db_value, _ in choices
    ]
    
    return max(*all_lengths)
