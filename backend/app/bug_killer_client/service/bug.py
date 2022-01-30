import bug_killer_client.network.bug as bug_client

from bug_killer_schemas.request.bug import CreateBugPayload, UpdateBugPayload
from bug_killer_schemas.response.bug import BugResponse


async def get_bug(auth: str, bug_id: str) -> BugResponse:
    """
    Get a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to get
    """
    raw_rsp = await bug_client.get_project(auth, bug_id)
    return BugResponse.from_dict(raw_rsp)


async def create_bug(auth: str, payload: CreateBugPayload) -> BugResponse:
    """
    Creates a bug
    auth: The cognito user's id token
    payload: Details of the bug to create
    """
    raw_rsp = await bug_client.create_bug(auth, payload.to_dict())
    return BugResponse.from_dict(raw_rsp)


async def update_bug(auth: str, payload: UpdateBugPayload) -> BugResponse:
    """
    Updates a bug by its id
    auth: The cognito user's id token
    payload: Details of the bug to update
    """
    raw_rsp = await bug_client.update_bug(auth, payload.to_dict())
    return BugResponse.from_dict(raw_rsp)


async def resolve_bug(auth: str, bug_id: str) -> BugResponse:
    """
    Resolves a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to resolve
    """
    raw_rsp = await bug_client.resolve_bug(auth, bug_id)
    return BugResponse.from_dict(raw_rsp)


async def delete_bug(auth: str, bug_id: str) -> BugResponse:
    """
    Deletes a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to delete
    """
    raw_rsp = await bug_client.delete_bug(auth, bug_id)
    return BugResponse.from_dict(raw_rsp)
