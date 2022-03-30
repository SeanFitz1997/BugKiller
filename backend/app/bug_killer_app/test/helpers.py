import json
import socket
from time import sleep
from typing import Optional, Dict, List, Any

from bug_killer_app.domain.response import HttpStatusCode
from bug_killer_utils.collections import is_jsonable


def wait_for_port_to_open(
        port: int,
        attempts: int = 3,
        attempt_wait: float = 0.5
) -> None:
    while attempts:
        if is_port_open(port):
            return
        sleep(attempt_wait)
        attempts -= 1

    raise TimeoutError(f'Port {port} did not open')


def is_port_open(port: int) -> bool:
    ddb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check = ddb_socket.connect_ex(('127.0.0.1', port))
    ddb_socket.close()
    return check == 0


def create_event(
        headers: Optional[Dict] = None,
        path: Optional[Dict] = None,
        query: Optional[Dict] = None,
        body: Optional[Dict] = None,
        request_context: Optional[Dict] = None
) -> Dict:
    return {
        'headers': headers or {},
        'pathParameters': path or {},
        'queryStringParameters': query or {},
        'body': json.dumps(body) if body else None,
        'requestContext': request_context or {}
    }


def create_cognito_authorizer_request_context(user_name: str) -> Dict:
    return {'authorizer': {'claims': {'cognito:username': user_name}}}


def assert_response(
        rsp: Dict[str, Any],
        expected_status: Optional[HttpStatusCode] = None,
        expected_body: Optional[dict] = None
) -> None:
    assert is_jsonable(rsp)
    if expected_status is not None:
        assert_response_status(rsp, expected_status)
    if expected_body is not None:
        assert_response_body(rsp, expected_body)


def assert_response_status(rsp: Dict[str, Any], status_code: HttpStatusCode) -> None:
    assert rsp['statusCode'] == status_code.value


def assert_response_body(rsp: Dict[str, Any], body: Dict) -> None:
    rsp_body = json.loads(rsp['body'])
    assert rsp_body == body


def assert_dict_attributes_not_none(data: Dict, attributes: List) -> None:
    for attr in attributes:
        assert data[attr] is not None


def assert_dict_attributes_equals(data: Dict, value_checks: Dict) -> None:
    for k, v in value_checks.items():
        assert data[k] == v
