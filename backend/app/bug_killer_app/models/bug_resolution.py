import arrow

from bug_killer_api_interface.schemas.entities.bug import BugResolution
from bug_killer_app.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute


class BkAppBugResolution(BugResolution):

    @classmethod
    def from_db_attribute(cls: type, db_attribute: BugResolutionMapAttribute) -> 'BkAppBugResolution':
        return cls(
            resolver_id=db_attribute.resolver_id,
            resolved_on=arrow.get(db_attribute.resolved_on)
        )

    def to_db_attribute(self) -> BugResolutionMapAttribute:
        return BugResolutionMapAttribute(
            resolver_id=self.resolver_id,
            resolved_on=self.resolved_on.datetime
        )
