from typing import Any, Dict

from bug_killer_app.access.entities.permission import assert_user_has_project_member_access
from bug_killer_app.access.entities.project import create_project, delete_project, get_users_projects, update_project, \
    get_project
from bug_killer_app.domain.api_handler import lambda_api_handler
from bug_killer_app.domain.request import get_path_param, get_auth_user, parse_dto, get_event_body
from bug_killer_app.domain.response import OkResponse, UpdatedResponse, CreatedResponse, DeletedResponse
from bug_killer_schemas.request.project import CreateProjectPayload, UpdateProjectPayload
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse


@lambda_api_handler
async def get_user_projects_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)

    manager_projects, member_projects = await get_users_projects(user_id)

    rsp = UserProjectsResponse(manager_projects=manager_projects, member_projects=member_projects)
    return OkResponse(body=rsp.api_dict()).api_dict()


@lambda_api_handler
async def get_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')

    project = await get_project(project_id)
    assert_user_has_project_member_access(user_id, project)

    rsp = ProjectResponse(project=project)
    return OkResponse(body=rsp.api_dict()).api_dict()


@lambda_api_handler
async def create_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    payload = parse_dto(get_event_body(evt), CreateProjectPayload)

    project = await create_project(user_id, payload)

    rsp = ProjectResponse(project=project)
    return CreatedResponse(body=rsp.api_dict()).api_dict()


@lambda_api_handler
async def update_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')
    payload = parse_dto(get_event_body(evt), UpdateProjectPayload)

    project = await update_project(user_id, project_id, payload)

    rsp = ProjectResponse(project=project)
    return UpdatedResponse(body=rsp.api_dict()).api_dict()


@lambda_api_handler
async def delete_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')

    project = await delete_project(user_id, project_id)

    rsp = ProjectResponse(project=project)
    return DeletedResponse(body=rsp.api_dict()).api_dict()
