import logging
from typing import Any, Dict

import requests

from bug_killer_client.domain.enviorment import ApiVariables
from bug_killer_client.util import get_auth_headers, handle_rsp


async def get_user_projects(auth: str) -> Dict[str, Any]:
    logging.info(f'Getting user projects')
    rsp = requests.get(ApiVariables.API_URL + '/projects', headers=get_auth_headers(auth))
    return handle_rsp(rsp)


async def get_project(auth: str, project_id: str) -> Dict[str, Any]:
    logging.info(f'Getting project by {project_id = }')
    rsp = requests.get(ApiVariables.API_URL + f'/projects/{project_id}', headers=get_auth_headers(auth))
    return handle_rsp(rsp)


async def create_project(auth: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    logging.info(f'Creating project with {payload = }')
    rsp = requests.post(ApiVariables.API_URL + '/projects', data=payload, headers=get_auth_headers(auth))
    return handle_rsp(rsp)


async def update_project(auth: str, project_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    logging.info(f'Updating project with {payload = }')
    rsp = requests.patch(
        ApiVariables.API_URL + f'/projects/{project_id}',
        data=payload, headers=get_auth_headers(auth)
    )
    return handle_rsp(rsp)


async def delete_project(auth: str, project_id: str) -> Dict[str, Any]:
    logging.info(f'Deleting project by {project_id = }')
    rsp = requests.delete(ApiVariables.API_URL + f'/projects/{project_id}', headers=get_auth_headers(auth))
    return handle_rsp(rsp)
