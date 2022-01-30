import json
from typing import List, Union, Dict, Any, Optional, TypeVar

from bug_killer_utils.strings import snake_case_to_camel_case, camel_case_to_snake_case


T = TypeVar('T')


def flatten(lst: List[Union[List, T]]) -> List[T]:
    if len(lst) == 0:
        return []

    head, tail = lst[0], lst[1:]
    flat_head = flatten(head) if isinstance(head, (list, tuple)) else [head]
    return flat_head + flatten(tail)


def add_to_dict_if_exists(data: Dict, key: Any, value: Optional[Any]) -> Dict:
    if value is not None:
        data[key] = value


def is_jsonable(data: Dict) -> bool:
    try:
        json.dumps(data)
        return True
    except Exception:
        return False


def is_dict_empty(data: Dict) -> bool:
    if len(data) == 0:
        return True
    return all(value is None for value in data.values())


def remove_none_values_from_dict(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if v is not None}


def remove_duplicates_in_list(x: List) -> List:
    return list(set(x))


def keys_to_camel_case(data: Dict[str, Any]) -> Dict[str, Any]:
    return {snake_case_to_camel_case(k): v for k, v in data.items()}


def keys_to_snake_case(data: Dict[str, Any]) -> Dict[str, Any]:
    return {camel_case_to_snake_case(k): v for k, v in data.items()}
