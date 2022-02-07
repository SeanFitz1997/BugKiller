import logging
from typing import Dict, Any

from requests import Response


def get_auth_headers(auth: str) -> Dict[str, str]:
    return {'Authorization': auth}


def handle_rsp(rsp: Response) -> Dict[str, Any]:
    """ Checks for rsp error status, and receives rsp json """
    rsp.raise_for_status()
    rsp = rsp.json()
    logging.info(f'Got {rsp = }')
    return rsp
