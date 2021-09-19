import json
from typing import List, Union, Dict, Any, Optional

from bug_killer.util.type_util import T


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
