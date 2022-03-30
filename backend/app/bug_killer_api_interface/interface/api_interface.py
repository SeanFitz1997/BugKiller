from bug_killer_api_interface.domain.api.api_interface import ApiInterface
from bug_killer_api_interface.domain.endpoint.endpoint import EndpointGroup
from bug_killer_api_interface.interface.endpoint.bug import GET_BUG, CREATE_BUG, UPDATE_BUG, RESOLVE_BUG, DELETE_BUG
from bug_killer_api_interface.interface.endpoint.project import GET_USER_PROJECTS, GET_PROJECT, CREATE_PROJECT, \
    UPDATE_PROJECT, DELETE_PROJECT


BUG_KILLER_API = ApiInterface(
    title='Bug Killer API',
    api_version='1.0.0',
    description='Bug Killer is a project management application where users can create projects, '
                'assign bugs to them and resolve them.',
    endpoint_groups=[
        EndpointGroup(
            name='Project',
            endpoints=[GET_USER_PROJECTS, GET_PROJECT, CREATE_PROJECT, UPDATE_PROJECT, DELETE_PROJECT]
        ),
        EndpointGroup(
            name='Bug',
            endpoints=[GET_BUG, CREATE_BUG, UPDATE_BUG, RESOLVE_BUG, DELETE_BUG]
        )
    ]
)
