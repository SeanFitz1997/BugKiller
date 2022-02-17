from bug_killer_schemas.entities.bug import Bug
from bug_killer_utils.model.bk_base_model import BkBaseModel


class BugResponse(BkBaseModel):
    """ Details on a single bug """
    project_id: str
    bug: Bug
