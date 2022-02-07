import json
from abc import ABC
from typing import Any, Dict

from arrow import Arrow
from pydantic import BaseModel

from bug_killer_utils.dates import to_utc_str
from bug_killer_utils.strings import snake_case_to_camel_case


class BKBaseConfig:
    arbitrary_types_allowed = True
    json_encoders = {Arrow: lambda dt: to_utc_str(dt)}
    alias_generator = snake_case_to_camel_case
    allow_population_by_field_name = True


class BkBaseModel(BaseModel, ABC):
    __config__ = BKBaseConfig

    def api_dict(self) -> Dict[str, Any]:
        return json.loads(self.json(by_alias=True))
