from typing import List, NoReturn, Union


def sort_by_create_date(items: List[Union['Project', 'Bug']]) -> NoReturn:
    items.sort(key=lambda x: x.created_on, reverse=True)
