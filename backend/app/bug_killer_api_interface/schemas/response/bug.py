import uuid
from typing import Optional

from bug_killer_api_interface.schemas.entities.bug import Bug
from bug_killer_utils.model.bk_base_model import BkBaseModel


class BugResponse(BkBaseModel):
    """ Details on a single bug """
    project_id: str
    bug: Bug

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            project_id: Optional[str] = None,
            bug: Optional[Bug] = None
    ):
        return BugResponse(
            project_id=project_id or str(uuid.uuid4()),
            bug=bug or Bug.test_double()
        )
