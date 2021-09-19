from typing import Any, Dict

from bug_killer.domain.exceptions import MissingAuthHeaderException, MissingRequiredRequestParamException


NO_DEFAULT = object()


def _get_param(evt: Dict[str, Any], param_type: str, param_name: str, default=NO_DEFAULT) -> Any:
    try:
        params = evt[param_type] or {}
        return params[param_name]
    except KeyError:
        if default is not NO_DEFAULT:
            return default
        else:
            raise MissingRequiredRequestParamException(param_type, param_name)


def get_body_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, 'body', param_name)


def get_header_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, 'headers', param_name)


def get_path_param(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, 'pathParameters', param_name)


def get_query_parma(evt: Dict[str, Any], param_name: str) -> Any:
    return _get_param(evt, 'queryStringParameters', param_name)


def get_optional_body_param(evt: Dict[str, Any], param_name: str, default=None) -> Any:
    return _get_param(evt, 'body', param_name, default=default)


def get_optional_query_param(evt: Dict[str, Any], param_name: str, default=None) -> Any:
    return _get_param(evt, 'queryStringParameters', param_name, default=default)


def get_auth_header(evt: Dict[str, Any]) -> str:
    try:
        return get_header_param(evt, 'cognito:username')
    except MissingRequiredRequestParamException:
        raise MissingAuthHeaderException()
