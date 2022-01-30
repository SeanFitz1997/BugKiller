import uuid
from typing import Optional, List

import arrow
from arrow import Arrow

from bug_killer_schemas.models.bug import BugResolution, Bug
from bug_killer_schemas.test.doubles.default_values import mock_bug_title, mock_bug_description, mock_bug_tags


def create_test_bug(
        bug_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_on: Optional[Arrow] = None,
        last_updated_on: Optional[Arrow] = None,
        resolved: Optional[BugResolution] = None,
) -> Bug:
    return Bug(
        id=bug_id or str(uuid.uuid4()),
        title=title or mock_bug_title,
        description=description or mock_bug_description,
        tags=tags or mock_bug_tags,
        created_on=created_on or arrow.utcnow(),
        last_updated_on=last_updated_on or arrow.utcnow(),
        resolved=resolved,
    )
