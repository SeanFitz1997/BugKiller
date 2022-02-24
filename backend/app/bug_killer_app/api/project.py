from typing import Any, Dict

from bug_killer_app.access.entities.permission import assert_user_has_project_member_access
from bug_killer_app.access.entities.project import create_project, delete_project, get_users_projects, update_project, \
    get_project
from bug_killer_app.domain.api_handler import lambda_api_handler, ApiEndpointDetails, HttpMethod, PathDetails, \
    ParamArgDetails
from bug_killer_app.domain.request import get_path_param, get_auth_user, parse_dto, get_event_body
from bug_killer_app.domain.response import HttpStatusCodes, HttpResponse
from bug_killer_schemas.request.project import CreateProjectPayload, UpdateProjectPayload
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(path='/projects/'),
        method=HttpMethod.GET,
        status=HttpStatusCodes.OK_STATUS,
        response_model=UserProjectsResponse
    )
)
async def get_user_projects_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Get all the projects that the user is a manager or member of """
    user_id = get_auth_user(evt)

    manager_projects, member_projects = await get_users_projects(user_id)

    rsp_model = get_user_projects_handler.endpoint_details.response_model
    rsp_status = get_user_projects_handler.endpoint_details.status

    rsp = rsp_model(manager_projects=manager_projects, member_projects=member_projects)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/projects/{projectId}',
            args=[
                ParamArgDetails(name='projectId', description='The id of the project to get')
            ]
        ),
        method=HttpMethod.GET,
        status=HttpStatusCodes.OK_STATUS,
        response_model=ProjectResponse
    )
)
async def get_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Gets a project by its id """
    user_id = get_auth_user(evt)

    project_id = get_path_param(evt, 'projectId')

    project = await get_project(project_id)
    assert_user_has_project_member_access(user_id, project)

    endpoint_details = get_project_handler.endpoint_details
    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(path='/projects/'),
        method=HttpMethod.POST,
        payload_model=CreateProjectPayload,
        status=HttpStatusCodes.CREATED_STATUS,
        response_model=ProjectResponse
    )
)
async def create_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Creates a new project, managed by the requestor """
    user_id = get_auth_user(evt)

    payload_model = create_project_handler.endpoint_details.payload_model
    payload = parse_dto(get_event_body(evt), payload_model)

    project = await create_project(user_id, payload)

    endpoint_details = create_project_handler.endpoint_details
    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/projects/{projectId}',
            args=[
                ParamArgDetails(name='projectId', description='The id of the project to update')
            ]
        ),
        method=HttpMethod.PATCH,
        payload_model=UpdateProjectPayload,
        status=HttpStatusCodes.OK_STATUS,
        response_model=ProjectResponse
    )
)
async def update_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Updates an existing project by its id """
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')
    payload_model = update_project_handler.endpoint_details.payload_model
    payload = parse_dto(get_event_body(evt), payload_model)

    project = await update_project(user_id, project_id, payload)

    rsp_model = update_project_handler.endpoint_details.response_model
    rsp_status = update_project_handler.endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/projects/{projectId}',
            args=[ParamArgDetails(name='projectId', description='The id of the project to delete')]
        ),
        method=HttpMethod.DELETE,
        status=HttpStatusCodes.OK_STATUS,
        response_model=ProjectResponse
    )
)
async def delete_project_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Deletes an existing project by its id """
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')

    project = await delete_project(user_id, project_id)

    rsp_model = delete_project_handler.endpoint_details.response_model
    rsp_status = delete_project_handler.endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()
