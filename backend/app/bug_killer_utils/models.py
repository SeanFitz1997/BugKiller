from abc import ABC
from dataclasses import asdict
from typing import Any, Dict, List

from bug_killer_utils.collections import keys_to_camel_case, keys_to_snake_case
from bug_killer_utils.strings import find_all_text_in_single_quotes


class MissingFromDictArgs(Exception):

    def __init__(self, subject_cls: type, from_dict_data: Dict[str, Any], missing_args: List[str]):
        self.subject_cls = subject_cls
        self.from_dict_data = from_dict_data
        self.missing_args = missing_args
        super().__init__(
            f'Failed to construct instance of class {self.subject_cls} from data {self.from_dict_data}. '
            f'Missing required args {self.missing_args}'
        )


class DefaultDictCasting(ABC):
    """ Provides default to and from dict methods to dataclasses """

    def to_dict(self) -> Dict[str, Any]:
        return keys_to_camel_case(asdict(self))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        try:
            return cls(**keys_to_snake_case(data))
        except TypeError as e:
            error_msg = e.args[0]
            missing_args = find_all_text_in_single_quotes(error_msg)
            raise MissingFromDictArgs(cls, data, missing_args) from e
