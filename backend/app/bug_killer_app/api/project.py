from aws_lambda_powertools.utilities.typing import LambdaContext

from bug_killer_api_interface.domain.endpoint.endpoint import EndpointDetails
from bug_killer_api_interface.interface.endpoint.project import DELETE_PROJECT, UPDATE_PROJECT, CREATE_PROJECT, \
    GET_PROJECT, GET_USER_PROJECTS
from bug_killer_app.access.entities.permission import assert_user_has_project_member_access
from bug_killer_app.access.entities.project import create_project, delete_project, get_users_projects, update_project, \
    get_project
from bug_killer_app.domain.api_handler import lambda_api_handler
from bug_killer_app.domain.request import get_path_param, get_auth_user, parse_dto, get_event_body
from bug_killer_app.domain.response import HttpResponse
from bug_killer_app.domain.types import ApiGatewayEvt


@lambda_api_handler(GET_USER_PROJECTS)
async def get_user_projects_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)

    manager_projects, member_projects = await get_users_projects(user_id)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(manager_projects=manager_projects, member_projects=member_projects)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(GET_PROJECT)
async def get_project_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)

    project_id = get_path_param(evt, 'projectId')

    project = await get_project(project_id)
    assert_user_has_project_member_access(user_id, project)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(CREATE_PROJECT)
async def create_project_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)

    payload_model = endpoint_details.payload_model
    payload = parse_dto(get_event_body(evt), payload_model)

    project = await create_project(user_id, payload)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(UPDATE_PROJECT)
async def update_project_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')
    payload_model = endpoint_details.payload_model
    payload = parse_dto(get_event_body(evt), payload_model)

    project = await update_project(user_id, project_id, payload)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(DELETE_PROJECT)
async def delete_project_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    project_id = get_path_param(evt, 'projectId')

    project = await delete_project(user_id, project_id)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project=project)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())
