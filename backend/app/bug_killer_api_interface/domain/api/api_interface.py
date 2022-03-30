from typing import Optional, Any

from apispec import APISpec
from pydantic.schema import schema

from bug_killer_api_interface.domain.endpoint.endpoint import EndpointGroup, EndpointDetails
from bug_killer_api_interface.domain.endpoint.parameter import ArgDetails, ParamTypes
from bug_killer_utils.collections import flatten
from bug_killer_utils.model.bk_base_model import BkBaseModel
from bug_killer_utils.strings import is_blank


OPEN_API_VERSION = '3.0.0'


class ApiInterface(BkBaseModel):
    title: str
    api_version: str
    description: str
    endpoint_groups: list[EndpointGroup]

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            title: Optional[str] = None,
            api_version: Optional[str] = None,
            description: Optional[str] = None,
            endpoint_groups: list[EndpointGroup] = None,
    ) -> 'ApiInterface':
        return cls(
            title=title or 'Test API',
            api_version=api_version or '1.0.0',
            description=description or 'A test API',
            endpoint_groups=endpoint_groups or [EndpointGroup.test_double()]
        )

    def to_open_api_doc(self) -> APISpec:
        # Create Open API Document
        api_doc = APISpec(
            title=self.title,
            version=self.api_version,
            openapi_version=OPEN_API_VERSION,
            info={'description': self.description}
        )

        for endpoint_group in self.endpoint_groups:
            ApiInterface._add_endpoint_group_to_open_api(api_doc, endpoint_group)

        ApiInterface._add_models_to_api(api_doc, self._get_api_models())
        ApiInterface._add_security_schema_models(api_doc, self.endpoint_groups)

        return api_doc

    @staticmethod
    def _add_models_to_api(api_doc: APISpec, models: list[type[BkBaseModel]]) -> None:
        top_level_schema = schema(models, ref_prefix='#/components/schemas/')
        for model_name, model_schema in top_level_schema['definitions'].items():
            api_doc.components.schema(model_name, model_schema)

    @staticmethod
    def _add_security_schema_models(api_doc: APISpec, endpoint_groups: list[EndpointGroup]) -> None:
        endpoints = flatten([group.endpoints for group in endpoint_groups])
        schemas = [endpoint.security_schema for endpoint in endpoints]

        seen_schemas: set[str] = set()
        for schema in schemas:
            if schema.name not in seen_schemas:
                api_doc.components.security_scheme(schema.name, schema.parameter.api_dict())
                seen_schemas.add(schema.name)

    @staticmethod
    def _add_endpoint_group_to_open_api(api_doc: APISpec, endpoint_group: EndpointGroup) -> None:
        for endpoint in endpoint_group.endpoints:
            path_parameters = ApiInterface._create_parameters_details(
                ParamTypes.PATH, endpoint.path_details.path_params)

            api_doc.path(
                path=endpoint.path_details.path,
                operations={
                    endpoint.method.value: {
                        'operationId': endpoint.operation_id,
                        'tags': [endpoint_group.name],
                        'description': endpoint.description,
                        'parameters': path_parameters,
                        'responses': ApiInterface._create_response_details(endpoint),
                        **({'security': [{endpoint.security_schema.name: []}]} if endpoint.security_schema else {}),
                        **({'requestBody': request_body} if (
                            request_body := ApiInterface._create_request_body_details(endpoint)) else {})
                    }
                }
            )

    @staticmethod
    def _create_parameters_details(param_type: ParamTypes, params: list[ArgDetails]) -> list[dict[str, Any]]:
        return [
            {
                'name': arg.name,
                'in': param_type.value,
                'description': arg.description,
                'required': arg.is_required,
                'schema': {'type': 'string'}
            } for arg in params
        ]

    @staticmethod
    def _create_response_details(endpoint: EndpointDetails) -> dict[str, Any]:
        return {
            str(endpoint.status.value): {
                'description': ApiInterface._get_model_details(endpoint.response_model),
                'content': {
                    'application/json': {
                        'schema': endpoint.response_model.__name__
                    }
                }
            }
        }

    @staticmethod
    def _create_request_body_details(endpoint: EndpointDetails) -> Optional[dict[str, Any]]:
        if payload_model := endpoint.payload_model:
            return {
                'description': ApiInterface._get_model_details(payload_model),
                'required': True,
                'content': {
                    'application/json': {
                        'schema': payload_model.__name__
                    }
                }
            }
        else:
            return None

    def _get_api_models(self) -> list[type[BkBaseModel]]:
        endpoints = flatten([group.endpoints for group in self.endpoint_groups])
        models: list[type[BkBaseModel]] = []
        for endpoint in endpoints:
            models.append(endpoint.response_model)
            if endpoint.payload_model:
                models.append(endpoint.payload_model)

        return models

    @staticmethod
    def _get_model_details(model: type[BkBaseModel]) -> str:
        model_doc = model.__doc__
        if is_blank(model_doc):
            raise ValueError(
                f'Model {model.__name__} must have a non blank doc string but received {model_doc = }'
            )
        return model_doc.strip()
