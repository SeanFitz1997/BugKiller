from aws_lambda_powertools.utilities.typing import LambdaContext

from bug_killer_api_interface.domain.endpoint.endpoint import EndpointDetails
from bug_killer_api_interface.interface.endpoint.bug import CREATE_BUG, GET_BUG, UPDATE_BUG, RESOLVE_BUG, DELETE_BUG
from bug_killer_app.access.entities.bug import create_project_bug, delete_project_bug, resolve_project_bug, get_bug, \
    update_project_bug
from bug_killer_app.domain.api_handler import lambda_api_handler
from bug_killer_app.domain.request import get_auth_user, get_path_param, parse_dto, get_event_body
from bug_killer_app.domain.response import HttpResponse
from bug_killer_app.domain.types import ApiGatewayEvt


@lambda_api_handler(CREATE_BUG)
async def create_bug_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    payload = parse_dto(get_event_body(evt), endpoint_details.payload_model)

    bug = await create_project_bug(user_id, payload)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project_id=payload.project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(GET_BUG)
async def get_bug_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await get_bug(user_id, bug_id)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(UPDATE_BUG)
async def update_bug_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    payload = parse_dto(get_event_body(evt), endpoint_details.payload_model)

    project_id, bug = await update_project_bug(user_id, bug_id, payload)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(RESOLVE_BUG)
async def resolve_bug_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await resolve_project_bug(user_id, bug_id)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())


@lambda_api_handler(DELETE_BUG)
async def delete_bug_handler(
        evt: ApiGatewayEvt,
        _: LambdaContext,
        endpoint_details: EndpointDetails
) -> HttpResponse:
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await delete_project_bug(user_id, bug_id)

    rsp_model = endpoint_details.response_model
    rsp_status = endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict())
