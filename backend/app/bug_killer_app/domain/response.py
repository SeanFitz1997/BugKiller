import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Any

from bug_killer_utils.models import DefaultDictCasting


class HttpStatusCodes(int, Enum):
    OK_STATUS = 200
    CREATED_STATUS = 201
    BAD_REQUEST_STATUS = 400
    UNAUTHORIZED_STATUS = 401
    FORBIDDEN_STATUS = 403
    NOT_FOUND_STATUS = 404
    INTERNAL_SERVER_ERROR_STATUS = 500


@dataclass
class HttpResponse(DefaultDictCasting):
    status_code: HttpStatusCodes
    headers: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        self.headers = self.headers or {}
        self.body = self.body or {}

    _DEFAULT_HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True
    }

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['status'] = self.status_code.value
        return data

    def to_api_dict(self) -> Dict[str, Any]:
        data = self.to_dict()
        data['headers'] = {**data['headers'], **HttpResponse._DEFAULT_HEADERS}
        data['body'] = json.dumps(data['body'])

        return data


class OkResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.OK_STATUS, headers, body)


class UpdatedResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.OK_STATUS, headers, body)


class CreatedResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.CREATED_STATUS, headers, body)


class DeletedResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.OK_STATUS, headers, body)


class BadRequestResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.BAD_REQUEST_STATUS, headers, body)


class UnAuthorizedResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.UNAUTHORIZED_STATUS, headers, body)


class ForbiddenResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.FORBIDDEN_STATUS, headers, body)


class NotFoundResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.NOT_FOUND_STATUS, headers, body)


class InternalServerErrorResponse(HttpResponse):

    def __init__(self, headers: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None):
        super().__init__(HttpStatusCodes.INTERNAL_SERVER_ERROR_STATUS, headers, body)


def message_body(message: str) -> Dict[str, Any]:
    return {'message': message}
