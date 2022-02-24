from enum import Enum
from typing import List, Type, NoReturn, Callable, Dict, Any, Optional

from apispec import APISpec
from pydantic.schema import schema

from bug_killer_app.api import bug as bug_api_module
from bug_killer_app.api import project as project_api_module
from bug_killer_app.domain.api_handler import ParamArgDetails, ApiEndpointDetails
from bug_killer_schemas.request import bug as bug_request_module
from bug_killer_schemas.request import project as project_request_module
from bug_killer_schemas.response import bug as bug_response_module
from bug_killer_schemas.response import project as project_response_module
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.object import get_local_function_in_module
from bug_killer_utils.strings import snake_case_to_camel_case, is_blank


API_TITLE = 'Bug Killer API'
API_DESCRIPTION = 'Bug Killer is a project management application where users can create projects, ' \
                  'assign bugs to them and resolve them.'
BUG_KILLER_API_VERSION = '1.0.0'
OPEN_API_VERSION = '3.0.0'
API_DOC_OUTPUT_FILE_NAME = 'api_doc.yml'

COGNITO_SECURITY_SCHEMA_NAME = 'EndpointAuthorizer'
COGNITO_SECURITY_SCHEMA = {
    'type': 'apiKey',
    'name': 'Authorization',
    'in': 'header'
}


class OpenApiParamTypes(str, Enum):
    HEADER = 'header'
    COOKIE = 'cookie'
    PATH = 'path'
    QUERY = 'query'


def generated_bug_killer_api_doc():
    api = _create_bug_killer_api()
    with open(API_DOC_OUTPUT_FILE_NAME, 'w') as f:
        f.write(api.to_yaml())


def _create_bug_killer_api() -> APISpec:
    # Create Open API Document
    api_doc = APISpec(
        title=API_TITLE,
        version=BUG_KILLER_API_VERSION,
        openapi_version=OPEN_API_VERSION,
        info={'description': API_DESCRIPTION}
    )

    # Add path details
    _add_operations_to_api(api_doc, 'Project', get_local_function_in_module(project_api_module))
    _add_operations_to_api(api_doc, 'Bug', get_local_function_in_module(bug_api_module))

    # Add Schema details
    api_models = get_local_function_in_module(project_request_module) + \
                 get_local_function_in_module(bug_request_module) + \
                 get_local_function_in_module(project_response_module) + \
                 get_local_function_in_module(bug_response_module)
    _add_models_to_api(api_doc, api_models)
    _add_cognito_security_schemas(api_doc)

    return api_doc


def _add_models_to_api(api_doc: APISpec, models: List[Type[BkBaseModel]]) -> NoReturn:
    top_level_schema = schema(models, ref_prefix='#/components/schemas/')
    for model_name, model_schema in top_level_schema['definitions'].items():
        api_doc.components.schema(model_name, model_schema)


def _add_cognito_security_schemas(api_doc: APISpec) -> NoReturn:
    api_doc.components.security_scheme(COGNITO_SECURITY_SCHEMA_NAME, COGNITO_SECURITY_SCHEMA)


def _add_operations_to_api(api_doc: APISpec, group: str, operations: List[Callable]) -> NoReturn:
    for operation in operations:
        endpoint_details = operation.endpoint_details
        path_parameters = _create_parameters_details(OpenApiParamTypes.PATH, endpoint_details.path_details.args)

        api_doc.path(
            path=endpoint_details.path_details.path,
            operations={
                endpoint_details.method.value: {
                    'operationId': _get_operation_id(operation),
                    'tags': [group],
                    'description': _get_operation_description(operation),
                    'parameters': path_parameters,
                    'responses': _create_response_details(endpoint_details),
                    'security': [{COGNITO_SECURITY_SCHEMA_NAME: ['read']}],
                    **({'requestBody': request_body} if (request_body := _create_request_body_details(endpoint_details))
                       else {})
                }
            }
        )


def _create_request_body_details(endpoint_details: ApiEndpointDetails) -> Optional[Dict[str, Any]]:
    if payload_model := endpoint_details.payload_model:
        return {
            'description': _get_model_details(payload_model),
            'required': True,
            'content': {
                'application/json': {
                    'schema': payload_model.__name__
                }
            }
        }


def _create_response_details(endpoint_details: ApiEndpointDetails) -> Dict[str, Any]:
    return {
        endpoint_details.status.value: {
            'description': _get_model_details(endpoint_details.response_model),
            'content': {
                'application/json': {
                    'schema': endpoint_details.response_model.__name__
                }
            }
        }
    }


def _create_parameters_details(
        param_type: OpenApiParamTypes,
        params: List[ParamArgDetails]
) -> List[Dict[str, Any]]:
    return [
        {
            'name': arg.name,
            'in': param_type.value,
            'description': arg.description,
            'required': arg.is_required,
            'schema': {'type': 'string'}
        } for arg in params
    ]


def _get_operation_id(operation: Callable) -> str:
    return snake_case_to_camel_case(operation.__name__.replace('_handler', ''))


def _get_operation_description(operation: Callable) -> str:
    operation_doc = operation.__doc__
    if is_blank(operation_doc):
        raise ValueError(
            f'Operation {operation.__name__} must have a non blank doc string but received {operation_doc = }'
        )
    return operation_doc.strip()


def _get_model_details(model: BkBaseModel) -> str:
    model_doc = model.__doc__
    if is_blank(model_doc):
        raise ValueError(
            f'Model {model.__name__} must have a non blank doc string but received {model_doc = }'
        )
    return model_doc.strip()
