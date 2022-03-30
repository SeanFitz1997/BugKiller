from __future__ import annotations

import asyncio
import json
import logging
from functools import wraps
from typing import Callable

from aws_lambda_powertools.utilities.typing import LambdaContext

from bug_killer_api_interface.domain.endpoint.endpoint import EndpointDetails
from bug_killer_app.domain.exceptions import ApiException
from bug_killer_app.domain.response import message_body, HttpStatusCode, HttpResponse
from bug_killer_app.domain.types import ApiGatewayEvt, ApiGatewayRsp, AsyncLambdaHandler, ApiGatewayRspLambdaHandler


def lambda_api_handler(endpoint_details: EndpointDetails) -> Callable[[AsyncLambdaHandler], ApiGatewayRspLambdaHandler]:
    """
    Decorator that adds addition common logic for all Api lambdas. It will:
    * Log the evt & rsp
    * Parse the request body
    * Handle all known & unknown exceptions
    * Format the Api rsp

    This decorator will alter the function signature. It will:
    * It will call the handler synchronously
    * Add endpoint details as a function param
    * It will format the http response
    """

    def decorator(handler: AsyncLambdaHandler) -> ApiGatewayRspLambdaHandler:

        @wraps(handler)
        def wrapper(evt: ApiGatewayEvt, ctx: LambdaContext) -> ApiGatewayRsp:
            try:
                # Log un-formatted evt
                logging.info(f'evt = {json.dumps(evt)}')

                # Parse request body
                if evt.get('body'):
                    evt['body'] = json.loads(evt['body'])

                # Run async handler
                http_rsp = asyncio.run(handler(evt, ctx, endpoint_details))

            except ApiException as e:
                logging.exception('Known API exception')
                http_rsp = e.get_api_response()

            except Exception:
                logging.exception('Unknown exception. Returning Internal server error response')
                http_rsp = HttpResponse(
                    status_code=HttpStatusCode.INTERNAL_SERVER_ERROR_STATUS,
                    body=message_body('Internal server error')
                )

            # Convert Rsp to Api Gw dict
            api_gw_dict = http_rsp.api_dict()

            # Log Rsp & Evt
            logging.info(f'evt = {json.dumps(evt)}\nrsp = {json.dumps(api_gw_dict)}')

            return api_gw_dict

        return wrapper

    return decorator
