from typing import Optional, List

from bug_killer_schemas.request.bug import CreateBugPayload
from bug_killer_schemas.test.doubles.default_values import mock_bug_title, mock_bug_description, mock_bug_tags


def create_test_create_bug_payload(
        project_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
) -> CreateBugPayload:
    return CreateBugPayload(
        project_id,
        title or mock_bug_title,
        description or mock_bug_description,
        tags or mock_bug_tags
    )
