import json
from abc import ABC
from typing import Any, Dict, NoReturn, Type

from arrow import Arrow
from pydantic import BaseModel
from typing_extensions import ParamSpec

from bug_killer_utils.dates import to_utc_str
from bug_killer_utils.strings import snake_case_to_camel_case


P = ParamSpec('P')


class BKBaseConfig:
    arbitrary_types_allowed = True
    json_encoders = {Arrow: lambda dt: to_utc_str(dt)}
    alias_generator = snake_case_to_camel_case
    allow_population_by_field_name = True

    @staticmethod
    def schema_extra(schema: Dict[str, Any], model: Type['BkBaseModel']) -> NoReturn:
        if test_double := model.test_double():
            test_double_dict = test_double.api_dict()
            for prop_name, prop_details in schema.get('properties', {}).items():
                prop_details['example'] = test_double_dict[prop_name]


class BkBaseModel(BaseModel, ABC):
    __config__ = BKBaseConfig

    def api_dict(self) -> Dict[str, Any]:
        return json.loads(self.json(by_alias=True))

    @classmethod
    def test_double(cls, **kwargs: ParamSpec.kwargs) -> 'BkBaseModel':
        return None
