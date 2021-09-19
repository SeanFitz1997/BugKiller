from typing import Any, Dict

import arrow
from arrow import Arrow

from bug_killer.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer.util.dates import to_utc_str


class BugResolution:

    def __init__(self, resolver_id: str, resolved_on: Arrow):
        self.resolver_id = resolver_id
        self.resolved_on = resolved_on

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BugResolution":
        return BugResolution(
            resolver_id=data["resolverId"],
            resolved_on=arrow.get(data["resolvedOn"])
        )

    @staticmethod
    def from_db_attribute(db_attribute: BugResolutionMapAttribute) -> "BugResolution":
        return BugResolution(
            resolver_id=db_attribute.resolver_id,
            resolved_on=arrow.get(db_attribute.resolved_on)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resolverId": self.resolver_id,
            "resolvedOn": to_utc_str(self.resolved_on)
        }

    def __repr__(self) -> str:
        return str(self.to_dict())
