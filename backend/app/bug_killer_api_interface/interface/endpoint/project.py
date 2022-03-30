from bug_killer_api_interface.domain.endpoint.endpoint import EndpointDetails
from bug_killer_api_interface.domain.endpoint.parameter import PathDetails, ArgDetails
from bug_killer_api_interface.interface.security import BK_SECURITY_SCHEMA
from bug_killer_api_interface.schemas.request.project import CreateProjectPayload, UpdateProjectPayload
from bug_killer_api_interface.schemas.response.project import UserProjectsResponse, ProjectResponse
from bug_killer_utils.http import HttpMethod, HttpStatusCode


GET_USER_PROJECTS = EndpointDetails(
    operation_id='GetUserProjects',
    description='Get all the projects that the user is a manager or member of',
    method=HttpMethod.GET,
    path_details=PathDetails(
        path='/projects/',
    ),
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=UserProjectsResponse,
)

GET_PROJECT = EndpointDetails(
    operation_id='GetProject',
    description='Gets a project by its id',
    method=HttpMethod.GET,
    path_details=PathDetails(
        path='/projects/{projectId}',
        path_params=[
            ArgDetails(name='projectId', description='The id of the project to get')
        ]
    ),
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=ProjectResponse,
)

CREATE_PROJECT = EndpointDetails(
    operation_id='CreateProject',
    description='Creates a new project, managed by the requestor',
    method=HttpMethod.POST,
    path_details=PathDetails(
        path='/projects/',
    ),
    payload_model=CreateProjectPayload,
    status=HttpStatusCode.CREATED_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=ProjectResponse,
)

UPDATE_PROJECT = EndpointDetails(
    operation_id='UpdateProject',
    description='Updates an existing project by its id',
    method=HttpMethod.PATCH,
    path_details=PathDetails(
        path='/projects/{projectId}',
        path_params=[
            ArgDetails(name='projectId', description='The id of the project to update')
        ]
    ),
    payload_model=UpdateProjectPayload,
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=ProjectResponse,
)

DELETE_PROJECT = EndpointDetails(
    operation_id='DeleteProject',
    description='Delete an existing project by its id',
    method=HttpMethod.DELETE,
    path_details=PathDetails(
        path='/projects/{projectId}',
        path_params=[
            ArgDetails(name='projectId', description='The id of the project to delete')
        ]
    ),
    status=HttpStatusCode.OK_STATUS,
    security_schema=BK_SECURITY_SCHEMA,
    response_model=ProjectResponse,
)
