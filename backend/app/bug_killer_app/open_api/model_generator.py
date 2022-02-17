from typing import List, Type, NoReturn, Callable

from apispec import APISpec
from pydantic.schema import schema

from bug_killer_app.api import bug as bug_api_module
from bug_killer_app.api import project as project_api_module
from bug_killer_schemas.request import bug as bug_request_module
from bug_killer_schemas.request import project as project_request_module
from bug_killer_schemas.response import bug as bug_response_module
from bug_killer_schemas.response import project as project_response_module
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.object import get_local_function_in_module
from bug_killer_utils.strings import snake_case_to_camel_case


API_TITLE = 'Bug Killer API'
API_DESCRIPTION = 'Bug Killer is a project management application where users can create projects, ' \
                  'assign bugs to them and resolve them.'
API_VERSION = '1.0.0'
OPEN_API_VERSION = '3.0.0'
API_DOC_OUTPUT_FILE_NAME = 'api_doc.yml'


def generated_bug_killer_api_doc():
    api = _create_bug_killer_api()
    with open(API_DOC_OUTPUT_FILE_NAME, 'w') as f:
        f.write(api.to_yaml())


def _create_bug_killer_api() -> APISpec:
    # Create Open API Document
    api_doc = APISpec(
        title=API_TITLE,
        version=API_VERSION,
        openapi_version=OPEN_API_VERSION,
        info={'description': API_DESCRIPTION}
    )

    api_models = get_local_function_in_module(project_request_module) + \
                 get_local_function_in_module(bug_request_module) + \
                 get_local_function_in_module(project_response_module) + \
                 get_local_function_in_module(bug_response_module)
    _add_models_to_api(api_doc, api_models)

    api_operations = get_local_function_in_module(project_api_module) + get_local_function_in_module(bug_api_module)
    _add_operations_to_api(api_doc, api_operations)

    return api_doc


def _add_models_to_api(api_doc: APISpec, models: List[Type[BkBaseModel]]) -> NoReturn:
    top_level_schema = schema(models, ref_prefix='#/components/schemas/')
    for model_name, model_schema in top_level_schema['definitions'].items():
        api_doc.components.schema(model_name, model_schema)


def _add_operations_to_api(api_doc: APISpec, operations: List[Callable]) -> NoReturn:
    for operation in operations:
        endpoint_details = operation.endpoint_details

        parameters = [
            {
                'name': arg.name,
                'in': 'path',
                'description': arg.description,
                'required': arg.is_required,
                'schema': {'type': 'string'}
            } for arg in endpoint_details.path_details.args
        ]

        api_doc.path(
            path=endpoint_details.path_details.path,
            operations={
                endpoint_details.method.value: {
                    'description': operation.__doc__.strip(),
                    'parameters': parameters,
                    'operationId': snake_case_to_camel_case(operation.__name__.replace('_handler', '')),
                    'responses': {
                        endpoint_details.status.value: {
                            'description': endpoint_details.response_model.__doc__.strip(),
                            'content': {
                                'application/json': {
                                    'schema': endpoint_details.response_model.__name__
                                }
                            }
                        }
                    }
                }
            }
        )
