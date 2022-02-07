import asyncio
import json
import logging
from typing import Callable, Any, Dict

from bug_killer_app.domain.exceptions import UnauthorizedProjectAccessException, MissingAuthHeaderException, \
    MissingRequiredRequestParamException, NotFoundException, MultipleMatchException, ManagerNotFoundException, \
    EmptyUpdateException, NoChangesInUpdateException, AlreadyResolvedBugException
from bug_killer_app.domain.response import UnAuthorizedResponse, BadRequestResponse, NotFoundResponse, \
    InternalServerErrorResponse, message_body, ForbiddenResponse


def handle_exception_responses(handler: Callable) -> Callable:
    """
    Decoration that catches know and unknown exceptions from the API handler
    and returns a http response
    """

    def wrapper(*args, **kwargs) -> Dict[str, Any]:
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


def log_event_response(handler: Callable) -> Callable:
    """ Logs the input event and response as JSON """

    def wrapper(*args, **kwargs) -> Any:
        evt = args[0]
        logging.info(f'evt = {json.dumps(evt)}')
        rsp = handler(*args, **kwargs)
        logging.info(f'rsp = {json.dumps(rsp)}')
        return rsp

    return wrapper


def parse_body(handler: Callable) -> Callable:
    """ Parse the json str in evt['body'] in place """

    def wrapper(*args, **kwargs) -> Any:
        evt = args[0]
        if evt.get('body'):
            evt['body'] = json.loads(evt['body'])
        return handler(*args, **kwargs)

    return wrapper


def lambda_api_handler(handler: Callable) -> Callable:
    """ Wraps all the API decorators in order. This should be attached to all API lambda handlers """

    @handle_exception_responses
    @log_event_response
    @parse_body
    def wrapper(*args, **kwargs) -> Any:
        return asyncio.run(handler(*args, **kwargs))

    return wrapper
