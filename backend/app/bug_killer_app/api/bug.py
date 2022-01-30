from typing import Any, Dict

from bug_killer_app.access.entities.bug import create_project_bug, delete_project_bug, resolve_project_bug, get_bug, \
    update_project_bug
from bug_killer_app.domain.api_handler import lambda_api_handler
from bug_killer_app.domain.request import get_auth_user, get_path_param, parse_dto, get_event_body
from bug_killer_app.domain.response import CreatedResponse, DeletedResponse, UpdatedResponse, OkResponse
from bug_killer_schemas.request.bug import UpdateBugPayload, CreateBugPayload
from bug_killer_schemas.response.bug import BugResponse


@lambda_api_handler
async def get_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await get_bug(user_id, bug_id)

    rsp = BugResponse(project_id, bug)
    return OkResponse(body=rsp.to_dict()).to_api_dict()


@lambda_api_handler
async def create_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    payload = parse_dto(get_event_body(evt), CreateBugPayload)

    bug = await create_project_bug(user_id, payload)

    rsp = BugResponse(payload.project_id, bug)
    return CreatedResponse(body=rsp.to_dict()).to_api_dict()


@lambda_api_handler
async def update_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')
    payload = parse_dto(get_event_body(evt), UpdateBugPayload)

    project_id, bug = await update_project_bug(user_id, bug_id, payload)

    rsp = BugResponse(project_id, bug)
    return UpdatedResponse(body=rsp.to_dict()).to_api_dict()


@lambda_api_handler
async def resolve_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await resolve_project_bug(user_id, bug_id)

    rsp = BugResponse(project_id, bug)
    return UpdatedResponse(body=rsp.to_dict()).to_api_dict()


@lambda_api_handler
async def delete_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await delete_project_bug(user_id, bug_id)

    rsp = BugResponse(project_id, bug)
    return DeletedResponse(body=rsp.to_dict()).to_api_dict()
