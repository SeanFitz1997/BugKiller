from datetime import datetime
from typing import Optional, Set

from bug_killer.models.bug import Bug


def create_test_bug(
        bug_id: Optional[str] = 'bug1',
        title: Optional[str] = 'test',
        description: Optional[str] = 'test bug',
        tags: Optional[Set[str]] = set(['test']),
        created_on: Optional[datetime] = None,
        last_updated_on: Optional[datetime] = None,
) -> Bug:
    if created_on is None:
        created_on = datetime.now()

    if last_updated_on is None:
        last_updated_on = datetime.now()

    return Bug(
        id=bug_id,
        title=title,
        description=description,
        tags=tags,
        created_on=created_on,
        last_updated_on=last_updated_on
    )
