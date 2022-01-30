import bug_killer_client.network.project as project_client
from bug_killer_schemas.request.project import CreateProjectPayload, UpdateProjectPayload
from bug_killer_schemas.response.project import UserProjectsResponse, ProjectResponse


async def get_user_projects(auth: str) -> UserProjectsResponse:
    """
    Get the projects that the user is a manager or member of
    auth: The cognito user's id token
    """
    raw_rsp = await project_client.get_user_projects(auth)
    return UserProjectsResponse.from_dict(raw_rsp)


async def get_project(auth: str, project_id: str) -> ProjectResponse:
    """
    Get project by its id
    auth: The cognito user's id token
    project_id: The id of the project to get
    """
    raw_rsp = await project_client.get_project(auth, project_id)
    return ProjectResponse.from_dict(raw_rsp)


async def create_project(auth: str, payload: CreateProjectPayload) -> ProjectResponse:
    """
    Creates a project
    auth: The cognito user's id token
    payload: The details of the project to create
    """
    raw_rsp = await project_client.create_project(auth, payload.to_dict())
    return ProjectResponse.from_dict(raw_rsp)


async def update_project(auth: str, project_id: str, payload: UpdateProjectPayload) -> ProjectResponse:
    """
    Updates a project by its id
    auth: The cognito user's id token
    project_id: The id of the project to update
    payload: The details of the project to update
    """
    raw_rsp = await project_client.update_project(auth, project_id, payload.to_dict())
    return ProjectResponse.from_dict(raw_rsp)


async def delete_project(auth: str, project_id: str) -> ProjectResponse:
    """
    Deletes a project by its id
    auth: The cognito user's id token
    project_id: The id of the project to delete
    """
    raw_rsp = await project_client.delete_project(auth, project_id)
    return ProjectResponse.from_dict(raw_rsp)
