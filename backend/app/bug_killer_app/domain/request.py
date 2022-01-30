from enum import Enum
from typing import Any, Dict

from bug_killer_app.domain.exceptions import MissingAuthHeaderException, MissingRequiredRequestParamException
from bug_killer_utils.models import MissingFromDictArgs
from bug_killer_utils.strings import snake_case_to_camel_case


NO_DEFAULT = object()


class ParameterType(str, Enum):
    BODY = 'body'
    HEADERS = 'headers'
    PATH = 'pathParameters'
    QUERY = 'queryStringParameters'
    CONTEXT = 'requestContext'


def _get_param(evt: Dict[str, Any], param_type: ParameterType, param_name: str, default=NO_DEFAULT) -> Any:
    try:
        params = evt[param_type.value] or {}
        return params[param_name]
    except KeyError:
        if default is not NO_DEFAULT:
            return default
        else:
            raise MissingRequiredRequestParamException(param_type, param_name)


def get_body_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, ParameterType.BODY, param_name)


def get_header_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, ParameterType.HEADERS, param_name)


def get_path_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, ParameterType.PATH, param_name)


def get_query_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, ParameterType.QUERY, param_name)


def get_optional_body_param(evt: Dict[str, Any], param_name: str, default=None) -> Any:
    return _get_param(evt, ParameterType.BODY, param_name, default=default)


def get_optional_query_param(evt: Dict[str, Any], param_name: str, default=None) -> Any:
    return _get_param(evt, ParameterType.QUERY, param_name, default=default)


def get_event_body(evt: Dict[str, Any]) -> Dict[str, Any]:
    return evt.get(ParameterType.BODY.value) or {}


def parse_dto(evt_body: Dict[str, Any], dto_class: type) -> object:
    try:
        return dto_class.from_dict(evt_body)
    except MissingFromDictArgs as e:
        raise MissingRequiredRequestParamException(
            ParameterType.BODY.value,
            snake_case_to_camel_case(e.missing_args[0])
        )


def get_auth_user(evt: Dict[str, Any]) -> str:
    try:
        request_ctx = evt[ParameterType.CONTEXT.value]
        claims = request_ctx['authorizer']['claims']
        return claims['cognito:username']
    except KeyError as e:
        raise MissingAuthHeaderException() from e
