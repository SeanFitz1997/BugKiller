import json
from typing import Any, Dict, Optional, NoReturn
from unittest.mock import MagicMock

from requests import Response

from bug_killer_client.domain.enviorment import ApiVariables


def create_mock_response(status: int, body: Optional[Dict[str, Any]] = None) -> Response:
    rsp = Response()
    rsp.status_code = status
    if body:
        rsp._content = str.encode(json.dumps(body))

    return rsp


def assert_expected_network_call(
        mock: MagicMock,
        resource_path: str,
        expected_body: Optional[Dict[str, Any]] = None,
        expected_headers: Optional[Dict[str, Any]] = None
) -> NoReturn:
    kwargs = {
        **({'data': expected_body} if expected_body else {}),
        **({'headers': expected_headers} if expected_headers else {})
    }
    expected_url = ApiVariables.API_URL + resource_path
    mock.assert_called_once_with(expected_url, **kwargs)
