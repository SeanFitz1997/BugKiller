from __future__ import annotations

import inspect
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from arrow import Arrow
from pydantic import BaseModel, BaseConfig
from typing_extensions import ParamSpec

from bug_killer_utils.dates import to_utc_str
from bug_killer_utils.strings import snake_case_to_camel_case


P = ParamSpec('P')


class BkBaseConfig(BaseConfig):
    arbitrary_types_allowed = True
    json_encoders = {Arrow: lambda dt: to_utc_str(dt)}
    alias_generator = snake_case_to_camel_case
    allow_population_by_field_name = True

    @staticmethod
    def schema_extra(schema: Dict[str, Any], model: Type['BkBaseModel']) -> None:  # type: ignore[override]
        # Ignoring error: Signature of "schema_extra" incompatible with supertype "BaseConfig"
        # Calling with types given in the docs https://pydantic-docs.helpmanual.io/usage/schema/
        if test_double := model.test_double():
            test_double_dict = test_double.api_dict()
            for prop_name, prop_details in schema.get('properties', {}).items():
                prop_details['example'] = test_double_dict[prop_name]


class BkBaseModel(BaseModel, ABC):
    __config__ = BkBaseConfig

    def __init_subclass__(cls, **kwargs: P.kwargs) -> None:  # type: ignore[name-defined]
        double_args = inspect.getfullargspec(cls.test_double)
        if len(double_args.args) > 1 or double_args.varargs is not None or double_args.varkw is not None:
            raise ValueError(
                'BkBaseModel sub classes must use key word only args in their test double methods, '
                f'But {cls.__name__} has args {double_args}'
            )

    def api_dict(self) -> Dict[str, Any]:
        return json.loads(self.json(by_alias=True))

    @classmethod
    @abstractmethod
    def test_double(cls, **kwargs: P.kwargs) -> 'BkBaseModel':  # type: ignore[name-defined]
        # MyPy does not yet support ParamSpec https://github.com/python/mypy/issues/8645
        pass
