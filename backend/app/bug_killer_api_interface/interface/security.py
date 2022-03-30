from bug_killer_api_interface.domain.endpoint.parameter import ParamTypes
from bug_killer_api_interface.domain.endpoint.security import SecuritySchema, SecuritySchemaParameter, SecurityType


BK_SECURITY_SCHEMA = SecuritySchema(
    name='EndpointAuthorizer',
    parameter=SecuritySchemaParameter(
        name='Authorization',
        type=SecurityType.API_KEY,
        in_=ParamTypes.HEADER
    )
)
