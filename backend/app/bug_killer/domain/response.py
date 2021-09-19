import logging
from typing import Dict, Optional, Any, Callable

from bug_killer.domain.exceptions import (
    MissingAuthHeaderException,
    MissingRequiredRequestParamException,
    UnauthorizedProjectAccessException,
    NotFoundException
)

import json

class HttpStatusCodes:
    OK_STATUS = 200
    CREATED_STATUS = 201
    BAD_REQUEST_STATUS = 400
    UNAUTHORIZED_STATUS = 401
    NOT_FOUND_STATUS = 404
    INTERNAL_SERVER_ERROR_STATUS = 500


class Response:

    def __init__(
            self,
            status: int,
            headers: Optional[Dict[str, Any]] = None,
            body: Optional[Dict[str, Any]] = None
    ):
        self.status = status
        self.headers = headers or {}
        self.body = body or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statusCode": self.status,
            "headers": self.headers,
            "body": self.body
        }

    def to_api_dict(self) -> str:
        data = self.to_dict()
        data['body'] = json.dumps(data['body'])
        return data

    def __repr__(self) -> str:
        return str(self.to_dict())


class OkResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.OK_STATUS, headers, body)


class UpdatedResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.OK_STATUS, headers, body)


class CreatedResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.CREATED_STATUS, headers, body)


class DeletedResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.OK_STATUS, headers, body)


class BadRequestResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.BAD_REQUEST_STATUS, headers, body)


class UnAuthorizedResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.UNAUTHORIZED_STATUS, headers, body)


class NotFoundResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.NOT_FOUND_STATUS, headers, body)


class InternalServerErrorResponse(Response):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.INTERNAL_SERVER_ERROR_STATUS, headers, body)


def message_body(message: str) -> Dict[str, Any]:
    return {'message': message}


def handle_exception_responses(handler: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except UnauthorizedProjectAccessException as e:
            return UnAuthorizedResponse(body=message_body(e.message)).to_api_dict()
        except MissingAuthHeaderException as e:
            return UnAuthorizedResponse(body=message_body(e.message)).to_api_dict()
        except MissingRequiredRequestParamException as e:
            return BadRequestResponse(body=message_body(e.message)).to_api_dict()
        except NotFoundException as e:
            return NotFoundResponse(body=message_body(e.message)).to_api_dict()
        except Exception:
            logging.exception('Uncaught exception. Returning Internal server error response')
            return InternalServerErrorResponse(body=message_body('Internal server error')).to_api_dict()

    return wrapper
