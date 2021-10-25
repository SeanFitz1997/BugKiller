import logging
from typing import Any, Dict

from bug_killer.access.entities import (
    create_project,
    delete_project,
    get_users_projects,
    update_project
)
from bug_killer.domain.request import (
    get_body_param,
    get_optional_body_param,
    get_path_param,
    get_auth_user
)
from bug_killer.domain.response import (
    OkResponse,
    UpdatedResponse,
    CreatedResponse,
    DeletedResponse,
    handle_exception_responses
)
from bug_killer.models.dto.project import (
    CreateProjectPayload,
    ProjectResponse,
    UpdateProjectPayload,
    UserProjectsResponse,
    DeleteProjectPayload
)


@handle_exception_responses
def get_user_projects_handler(evt: Dict[str, Any], ctx) -> Dict[str, Any]:
    print('HERE')
    print(f'{evt =}')
    print(f'{ctx =}, {dir(ctx)}')
    print(f'{ctx.identity}')
    print(f'{dir(ctx.identity)}')
    print(f'{ctx.identity.cognito_identity_id} , {ctx.identity.cognito_identity_pool_id}')
    user_id = get_auth_user(evt)
    manager_projects, member_projects = get_users_projects(user_id)
    rsp = UserProjectsResponse(manager_projects, member_projects)
    return OkResponse(body=rsp.to_dict()).to_api_dict()


@handle_exception_responses
def create_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    logging.info(f'{evt =}')
    user_id = get_auth_user(evt)
    payload = CreateProjectPayload(
        manager=user_id,
        title=get_body_param(evt, "title"),
        description=get_body_param(evt, "description"),
        members=get_optional_body_param(evt, "members", []),
        tags=get_optional_body_param(evt, "tags", []),
    )
    project = create_project(payload)
    rsp = ProjectResponse(project=project)
    return CreatedResponse(body=rsp.to_dict()).to_api_dict()


@handle_exception_responses
def update_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    logging.info(f'{evt =}')
    user_id = get_auth_user(evt)
    payload = UpdateProjectPayload(
        project_id=get_path_param(evt, 'projectId'),
        actor=user_id,
        title=get_optional_body_param(evt, "title"),
        description=get_optional_body_param(evt, "description"),
        manager=get_optional_body_param(evt, "manager"),
    )
    project = update_project(payload)
    rsp = ProjectResponse(project=project)
    return UpdatedResponse(body=rsp.to_dict()).to_api_dict()


@handle_exception_responses
def delete_project_handler(evt: Dict[str, Any], _):
    logging.info(f'{evt =}')
    user_id = get_auth_user(evt)
    payload = DeleteProjectPayload(
        actor=user_id,
        project_id=get_path_param(evt, "projectId")
    )
    project = delete_project(payload)
    rsp = ProjectResponse(project=project)
    return DeletedResponse(body=rsp.to_dict()).to_api_dict()
