from __future__ import annotations

from enum import Enum
from typing import Optional, Type

from bug_killer_api_interface.domain.endpoint.parameter import PathDetails
from bug_killer_api_interface.domain.endpoint.security import SecuritySchema
from bug_killer_api_interface.schemas.response.project import ProjectResponse
from bug_killer_utils.http import HttpMethod, HttpStatusCode
from bug_killer_utils.model.bk_base_model import BkBaseModel


class SecuritySchemaType(str, Enum):
    API_KEY = 'apiKey',
    HTTP = 'http',
    MUTUAL_TLS = 'mutualTLS',
    OAUTH2 = 'oauth2',
    OPEN_ID_CONNECT = 'openIdConnect'


class EndpointDetails(BkBaseModel):
    operation_id: str
    description: str
    path_details: PathDetails
    method: HttpMethod
    status: HttpStatusCode
    response_model: Type[BkBaseModel]
    payload_model: Optional[Type[BkBaseModel]] = None
    security_schema: Optional[SecuritySchema] = None

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            operation_id: Optional[str] = None,
            description: Optional[str] = None,
            path_details: Optional[PathDetails] = None,
            method: Optional[HttpMethod] = None,
            status: Optional[HttpStatusCode] = None,
            response_model: Optional[Type[BkBaseModel]] = None,
            payload_model: Optional[Type[BkBaseModel]] = None,
            security_schema: Optional[SecuritySchema] = None
    ) -> EndpointDetails:
        return cls(
            operation_id=operation_id or 'TestOperation',
            description='Test Operation',
            path_details=path_details or PathDetails.test_double(),
            method=method or HttpMethod.GET,
            status=status or HttpStatusCode.OK_STATUS,
            response_model=response_model or ProjectResponse,
            payload_model=payload_model or None,
            security_schema=security_schema
        )


class EndpointGroup(BkBaseModel):
    name: str
    endpoints: list[EndpointDetails]

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            name: Optional[str] = None,
            endpoints: Optional[EndpointDetails] = None
    ) -> 'EndpointGroup':
        return EndpointGroup(
            name=name or 'test',
            endpoints=endpoints or EndpointDetails.test_double()
        )
