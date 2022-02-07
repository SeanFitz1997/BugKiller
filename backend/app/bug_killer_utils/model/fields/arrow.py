from typing import Any

from arrow import Arrow

from bug_killer_utils.dates import try_parse_arrow


class ArrowField(Arrow):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Arrow:
        return try_parse_arrow(value)
