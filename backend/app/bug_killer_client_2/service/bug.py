import bug_killer_client.network.bug as bug_client

from bug_killer_api_interface.schemas.request import CreateBugPayload, UpdateBugPayload
from bug_killer_api_interface.schemas.response import BugResponse


async def get_bug(auth: str, bug_id: str) -> BugResponse:
    """
    Get a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to get
    """
    raw_rsp = await bug_client.get_bug(auth, bug_id)
    return BugResponse.parse_obj(raw_rsp)


async def create_bug(auth: str, payload: CreateBugPayload) -> BugResponse:
    """
    Creates a bug
    auth: The cognito user's id token
    payload: Details of the bug to create
    """
    raw_rsp = await bug_client.create_bug(auth, payload.api_dict())
    return BugResponse.parse_obj(raw_rsp)


async def update_bug(auth: str, bug_id: str, payload: UpdateBugPayload) -> BugResponse:
    """
    Updates a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to update
    payload: Details of the bug to update
    """
    raw_rsp = await bug_client.update_bug(auth, bug_id, payload.api_dict())
    return BugResponse.parse_obj(raw_rsp)


async def resolve_bug(auth: str, bug_id: str) -> BugResponse:
    """
    Resolves a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to resolve
    """
    raw_rsp = await bug_client.resolve_bug(auth, bug_id)
    return BugResponse.parse_obj(raw_rsp)


async def delete_bug(auth: str, bug_id: str) -> BugResponse:
    """
    Deletes a bug by its id
    auth: The cognito user's id token
    bug_id: The id of the bug to delete
    """
    raw_rsp = await bug_client.delete_bug(auth, bug_id)
    return BugResponse.parse_obj(raw_rsp)
