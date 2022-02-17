import asyncio
import json
import logging
from enum import Enum
from functools import wraps
from typing import Callable, TypeVar, Awaitable, Optional, Type, List

from pydantic import BaseModel, Field
from typing_extensions import ParamSpec

from bug_killer_app.domain.exceptions import UnauthorizedProjectAccessException, MissingAuthHeaderException, \
    MissingRequiredRequestParamException, NotFoundException, MultipleMatchException, ManagerNotFoundException, \
    EmptyUpdateException, NoChangesInUpdateException, AlreadyResolvedBugException
from bug_killer_app.domain.response import UnAuthorizedResponse, BadRequestResponse, NotFoundResponse, \
    InternalServerErrorResponse, message_body, ForbiddenResponse, HttpStatusCodes


P = ParamSpec('P')
R = TypeVar('R')


class HttpMethod(str, Enum):
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'
    DELETE = 'delete'


class PathArgDetails(BaseModel):
    name: str
    description: str
    is_required: bool = True


class PathDetails(BaseModel):
    path: str
    args: List[PathArgDetails] = Field(default_factory=list)

    # TODO Add validation of path and args


class ApiEndpointDetails(BaseModel):
    path_details: PathDetails
    method: HttpMethod
    status: HttpStatusCodes
    response_model: Type[BaseModel]
    payload_model: Optional[Type[BaseModel]] = None


def handle_exception_responses(handler: Callable[[P], R]) -> Callable[[P], R]:
    """
    Decoration that catches know and unknown exceptions from the API handler
    and returns a http response
    """

    @wraps(handler)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return handler(*args, **kwargs)

        # 400 Errors
        except (
                MissingRequiredRequestParamException, EmptyUpdateException, NoChangesInUpdateException,
                AlreadyResolvedBugException
        ) as e:
            logging.exception('Known 400 exception')
            return BadRequestResponse(body=message_body(e.message)).api_dict()

        # 401 Unauthorized Errors
        except MissingAuthHeaderException as e:
            logging.exception('Known 401 exception')
            return UnAuthorizedResponse(body=message_body(e.message)).api_dict()
        # 403 Forbidden Errors
        except UnauthorizedProjectAccessException as e:
            logging.exception('Known 403 exception')
            return ForbiddenResponse(body=message_body(e.message)).api_dict()

        # 404 Errors
        except NotFoundException as e:
            logging.exception('Known 404 exception')
            return NotFoundResponse(body=message_body(e.message)).api_dict()

        # 500 Errors
        except (ManagerNotFoundException, MultipleMatchException) as e:
            logging.exception('Known 500 exception')
            return InternalServerErrorResponse(body=message_body(e.message)).api_dict()
        except Exception:
            logging.exception('Unknown 500 exception. Returning Internal server error response')
            return InternalServerErrorResponse(body=message_body('Internal server error')).api_dict()

    return wrapper


def log_event_response(handler: Callable[[P], R]) -> Callable[[P], R]:
    """ Logs the input event and response as JSON """

    @wraps(handler)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        evt = args[0]
        logging.info(f'evt = {json.dumps(evt)}')
        rsp = handler(*args, **kwargs)
        logging.info(f'rsp = {json.dumps(rsp)}')
        return rsp

    return wrapper


def parse_body(handler: Callable[[P], R]) -> Callable[[P], R]:
    """ Parse the json str in evt['body'] in place """

    @wraps(handler)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        evt = args[0]
        if evt.get('body'):
            evt['body'] = json.loads(evt['body'])
        return handler(*args, **kwargs)

    return wrapper


def lambda_api_handler(endpoint_details: ApiEndpointDetails = None) -> Callable[[P], R]:
    """
     Wraps all the API decorators in order and
     adds endpoint description which is used to generate api docs and for generation for API GW infrastructure.
     This should be attached to all API lambda handlers
     """

    def decorator(handler: Callable[[P], Awaitable[R]]) -> Callable[[P], R]:
        @handle_exception_responses
        @log_event_response
        @parse_body
        @wraps(handler)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return asyncio.run(handler(*args, **kwargs))

        wrapper.endpoint_details = endpoint_details
        return wrapper

    return decorator
