from typing import Dict


def get_auth_headers(auth: str) -> Dict[str, str]:
    return {'Authorization': auth}
