from datetime import datetime

from pydantic import BaseModel

from bug_killer.datastore.attributes.bug_resolution_map import BugResolutionMapAttribute
from bug_killer.models.user import User


class BugResolution(BaseModel):
    resolved_id: User
    resolved_on: datetime


    @staticmethod
    def from_db_attribute(db_attribute: BugResolutionMapAttribute) -> 'BugResolution':
        # TODO: Get user by id

        return BugResolution(
            resolved_id=db_attribute.resolver_id,
            resolved_on=db_attribute.resolved_on
        )
