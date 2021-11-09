from typing import Any, Dict

from bug_killer.access.entities import (
    create_project_bug,
    delete_project_bug
)
from bug_killer.domain.request import get_body_param, get_optional_body_param, get_auth_user
from bug_killer.domain.response import CreatedResponse, DeletedResponse, handle_exception_responses
from bug_killer.models.dto.bug import (
    BugResponse,
    CreateBugPayload,
    DeleteBugPayload
)


@handle_exception_responses
def create_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    payload = CreateBugPayload(
        actor=user_id,
        project_id=get_body_param(evt, "projectId"),
        title=get_body_param(evt, "title"),
        description=get_body_param(evt, "description"),
        tags=get_optional_body_param(evt, "tags"),
    )
    bug = create_project_bug(payload)
    rsp = BugResponse(project_id=payload.project_id, bug=bug)
    return CreatedResponse(body=rsp.to_dict()).to_api_dict()


@handle_exception_responses
def delete_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    payload = DeleteBugPayload(
        actor=user_id,
        project_id=get_body_param(evt, "projectId"),
        bug_id=get_body_param(evt, "bugId")
    )
    bug = delete_project_bug(payload)
    rsp = BugResponse(project_id=payload.project_id, bug=bug)
    return DeletedResponse(body=rsp.to_dict()).to_api_dict()
