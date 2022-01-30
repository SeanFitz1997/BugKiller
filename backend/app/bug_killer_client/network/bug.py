import logging
from typing import Any, Dict

import requests

from bug_killer_client.domain.enviorment import ApiVariables
from bug_killer_client.util import get_auth_headers
from bug_killer_schemas.request.bug import CreateBugPayload


async def get_bug(auth: str, bug_id: str) -> Dict[str, Any]:
    logging.info(f'Getting bug by {bug_id = }')
    rsp = requests.get(ApiVariables.API_URL + f'/bugs/{bug_id}', headers=get_auth_headers(auth))
    rsp.raise_for_status()
    rsp = rsp.json()
    logging.info(f'Got {rsp = }')
    return rsp


async def create_bug(auth: str, payload: CreateBugPayload) -> Dict[str, Any]:
    logging.info(f'Creating bug with {payload = }')
    rsp = requests.post(ApiVariables.API_URL + '/bugs', data=payload, headers=get_auth_headers(auth))
    rsp.raise_for_status()
    rsp = rsp.json()
    logging.info(f'Got {rsp = }')
    return rsp


async def update_bug(auth: str, bug_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    logging.info(f'Updating bug {bug_id} with {payload = }')
    rsp = requests.patch(ApiVariables.API_URL + f'/bugs/{bug_id}', data=payload, headers=get_auth_headers(auth))
    rsp.raise_for_status()
    rsp = rsp.json()
    logging.info(f'Got {rsp = }')


async def resolve_bug(auth: str, bug_id: str) -> Dict[str, Any]:
    logging.info(f'Resolving bug {bug_id}')
    rsp = requests.patch(ApiVariables.API_URL + f'/bugs/{bug_id}', headers=get_auth_headers(auth))
    rsp.raise_for_status()
    rsp = rsp.json()
    logging.info(f'Got {rsp = }')
    return rsp


async def delete_bug(auth: str, bug_id: str) -> Dict[str, Any]:
    logging.info(f'Deleting bug by {bug_id = }')
    rsp = requests.delete(ApiVariables.API_URL + f'/bugs/{bug_id}', headers=get_auth_headers(auth))
    rsp.raise_for_status()
    rsp = rsp.json()
    logging.info(f'Got {rsp = }')
    return rsp
