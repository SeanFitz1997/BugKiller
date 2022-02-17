import uuid
from typing import Optional

from bug_killer_schemas.entities.bug import Bug
from bug_killer_schemas.response.bug import BugResponse
from bug_killer_schemas.test.doubles.models.bug import create_test_bug


def create_test_bug_rsp(
        project_id: Optional[str] = None,
        bug: Optional[Bug] = None
):
    return BugResponse(
        project_id=project_id or str(uuid.uuid4()),
        bug=bug or create_test_bug()
    )
