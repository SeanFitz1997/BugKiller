from typing import Any, Dict

from bug_killer_app.access.entities.bug import create_project_bug, delete_project_bug, resolve_project_bug, get_bug, \
    update_project_bug
from bug_killer_app.domain.api_handler import lambda_api_handler, ApiEndpointDetails, PathDetails, PathArgDetails, \
    HttpMethod
from bug_killer_app.domain.request import get_auth_user, get_path_param, parse_dto, get_event_body
from bug_killer_app.domain.response import HttpStatusCodes, \
    HttpResponse
from bug_killer_schemas.request.bug import CreateBugPayload
from bug_killer_schemas.response.bug import BugResponse


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/bugs/{bugId}',
            args=[
                PathArgDetails(name='bugId', description='The id of the bug to get')
            ]
        ),
        method=HttpMethod.GET,
        status=HttpStatusCodes.OK_STATUS,
        response_model=BugResponse
    )
)
async def get_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Gets a bug by its id """
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await get_bug(user_id, bug_id)

    rsp_model = get_bug_handler.endpoint_details.response_model
    rsp_status = get_bug_handler.endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(path='/bugs/'),
        method=HttpMethod.POST,
        status=HttpStatusCodes.CREATED_STATUS,
        response_model=BugResponse
    )
)
async def create_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Creates a new bug for a project """
    user_id = get_auth_user(evt)
    payload = parse_dto(get_event_body(evt), CreateBugPayload)

    bug = await create_project_bug(user_id, payload)

    rsp_model = get_bug_handler.endpoint_details.response_model
    rsp_status = get_bug_handler.endpoint_details.status

    rsp = rsp_model(project_id=payload.project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/bugs/{bugId}',
            args=[
                PathArgDetails(name='bugId', description='The id of the bug to update')
            ]
        ),
        method=HttpMethod.PATCH,
        status=HttpStatusCodes.OK_STATUS,
        response_model=BugResponse
    )
)
async def update_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Updates an existing bug by its id """
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    payload_model = update_bug_handler.endpoint_details.payload_model
    payload = parse_dto(get_event_body(evt), payload_model)

    project_id, bug = await update_project_bug(user_id, bug_id, payload)

    rsp_model = update_bug_handler.endpoint_details.response_model
    rsp_status = update_bug_handler.endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/bugs/{bugId}/resolve',
            args=[PathArgDetails(name='bugId', description='The id of the bug to resolve')]
        ),
        method=HttpMethod.PATCH,
        status=HttpStatusCodes.OK_STATUS,
        response_model=BugResponse
    )
)
async def resolve_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ resolves a bug by its id """
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await resolve_project_bug(user_id, bug_id)

    rsp_model = resolve_bug_handler.endpoint_details.response_model
    rsp_status = resolve_bug_handler.endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()


@lambda_api_handler(
    ApiEndpointDetails(
        path_details=PathDetails(
            path='/bugs/{bugId}',
            args=[PathArgDetails(name='bugId', description='The id of the bug to delete')]
        ),
        method=HttpMethod.DELETE,
        status=HttpStatusCodes.OK_STATUS,
        response_model=BugResponse
    )
)
async def delete_bug_handler(evt: Dict[str, Any], _) -> Dict[str, Any]:
    """ Deletes a bug by its id """
    user_id = get_auth_user(evt)
    bug_id = get_path_param(evt, 'bugId')

    project_id, bug = await delete_project_bug(user_id, bug_id)

    rsp_model = resolve_bug_handler.endpoint_details.response_model
    rsp_status = resolve_bug_handler.endpoint_details.status

    rsp = rsp_model(project_id=project_id, bug=bug)
    return HttpResponse(status_code=rsp_status, body=rsp.api_dict()).api_dict()
