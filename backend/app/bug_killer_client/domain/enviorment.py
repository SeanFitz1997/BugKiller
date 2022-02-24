import os
from typing import NoReturn


def set_api_url(url: str) -> NoReturn:
    ApiVariables.API_URL = url


class ApiVariables:
    class Defaults:
        API_URL = 'https://lay81tghjf.execute-api.eu-west-1.amazonaws.com/prod'


    # ATTN: This value can be updated
    API_URL = os.environ.get('API_URL', Defaults.API_URL)
