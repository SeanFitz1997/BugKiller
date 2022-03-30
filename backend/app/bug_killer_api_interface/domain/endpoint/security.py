from enum import Enum
from typing import Optional

from pydantic import Field

from bug_killer_api_interface.domain.endpoint.parameter import ParamTypes
from bug_killer_utils.model.bk_base_model import BkBaseModel


class SecurityType(str, Enum):
    API_KEY = 'apiKey'
    HTTP = 'http'
    MUTUAL_TLS = 'mutualTLS'
    OAUTH = 'oauth2'
    OPEN_ID_CONNECT = 'openIdConnect'


class SecuritySchemaParameter(BkBaseModel):
    type: SecurityType
    name: str
    in_: ParamTypes = Field(alias='in')

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            type: Optional[SecurityType] = None,
            name: Optional[str] = None,
            in_: Optional[ParamTypes] = None,
    ) -> 'SecuritySchemaParameter':
        return SecuritySchemaParameter(
            type=type or SecurityType.API_KEY,
            name=name or 'Authorizer',
            in_=in_ or ParamTypes.HEADER
        )


class SecuritySchema(BkBaseModel):
    name: str
    parameter: SecuritySchemaParameter

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            name: Optional[str] = None,
            parameter: Optional[SecuritySchemaParameter] = None
    ) -> 'SecuritySchema':
        return SecuritySchema(
            name=name or 'TestAuthorizer',
            parameter=parameter or SecuritySchemaParameter.test_double()
        )
