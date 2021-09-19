from typing import List, NoReturn


def remove_prefix(prefix: str, string: str) -> str:
    return string.split(prefix, maxsplit=1)[-1]


def sort_by_create_date(items: List['Project']) -> NoReturn:
    items.sort(key=lambda x: x.created_on, reverse=True)
