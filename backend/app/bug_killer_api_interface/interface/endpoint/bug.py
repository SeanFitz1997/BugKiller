from bug_killer_api_interface.domain.endpoint.endpoint import EndpointDetails
from bug_killer_api_interface.domain.endpoint.parameter import PathDetails, ArgDetails
from bug_killer_api_interface.interface.security import BK_SECURITY_SCHEMA
from bug_killer_api_interface.schemas.request.bug import CreateBugPayload, UpdateBugPayload
from bug_killer_api_interface.schemas.response.bug import BugResponse
from bug_killer_utils.http import HttpMethod, HttpStatusCode


GET_BUG = EndpointDetails(
    operation_id='GetBug',
    description='Get a bug by its id',
    method=HttpMethod.GET,
    path_details=PathDetails(
        path='/bug/{bugId}',
        path_params=[
            ArgDetails(name='bugId', description='The id of the bug to get')
        ]
    ),
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=BugResponse,
)

CREATE_BUG = EndpointDetails(
    operation_id='CreateBug',
    description='Create a bug for a project',
    method=HttpMethod.POST,
    path_details=PathDetails(path='/bug/'),
    payload_model=CreateBugPayload,
    status=HttpStatusCode.CREATED_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=BugResponse,
)

UPDATE_BUG = EndpointDetails(
    operation_id='UpdateBug',
    description='Update a bug by its id',
    method=HttpMethod.PATCH,
    path_details=PathDetails(
        path='/bug/{bugId}',
        path_params=[
            ArgDetails(name='bugId', description='The id of the bug to update')
        ]
    ),
    payload_model=UpdateBugPayload,
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=BugResponse,
)

RESOLVE_BUG = EndpointDetails(
    operation_id='ResolveBug',
    description='Resolve a bug by its id',
    method=HttpMethod.PATCH,
    path_details=PathDetails(
        path='/bug/{bugId}',
        path_params=[
            ArgDetails(name='bugId', description='The id of the bug to resolve')
        ]
    ),
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=BugResponse,
)

DELETE_BUG = EndpointDetails(
    operation_id='DeleteBug',
    description='Delete a bug by its id',
    method=HttpMethod.DELETE,
    path_details=PathDetails(
        path='/bug/{bugId}',
        path_params=[
            ArgDetails(name='bugId', description='The id of the bug to delete')
        ]
    ),
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=BugResponse,
)
