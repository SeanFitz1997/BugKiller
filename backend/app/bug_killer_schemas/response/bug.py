from dataclasses import dataclass
from typing import Dict, Any

from bug_killer_schemas.models.bug import Bug
from bug_killer_utils.models import DefaultDictCasting


@dataclass
class BugResponse(DefaultDictCasting):
    project_id: str
    bug: Bug

    _BUG_CLS = Bug

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['bug'] = self.bug.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Any:
        data['bug'] = BugResponse._BUG_CLS.from_dict(data['bug'])
        return super().from_dict(data)
