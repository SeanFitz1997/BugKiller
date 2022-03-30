from typing import List, Tuple, Any, Callable, Awaitable

from aws_lambda_powertools.utilities.typing import LambdaContext

from bug_killer_api_interface.domain.endpoint.endpoint import EndpointDetails
from bug_killer_app.datastore.project_table.project_item import ProjectItem
# All DDB items relating to a project
from bug_killer_app.domain.response import HttpResponse


AllProjectItems = Tuple[ProjectItem, ProjectItem, List[ProjectItem], List[ProjectItem]]

# The Api Gateway evt received by the lambda handler
ApiGatewayEvt = dict[str, Any]

# The Api Gateway dict that the lambda should return
ApiGatewayRsp = dict[str, Any]

# The function signature of the lambda handler before it is decorated
AsyncLambdaHandler = Callable[[ApiGatewayEvt, LambdaContext, EndpointDetails], Awaitable[HttpResponse]]

# The function signature of the lambda handler after it is decorated
ApiGatewayRspLambdaHandler = Callable[[ApiGatewayEvt, LambdaContext], ApiGatewayRsp]
