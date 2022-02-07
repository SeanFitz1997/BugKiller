from bug_killer_schemas.models.bug import Bug
from bug_killer_utils.model.bk_base_model import BkBaseModel


class BugResponse(BkBaseModel):
    project_id: str
    bug: Bug
