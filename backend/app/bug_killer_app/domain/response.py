import json
from enum import Enum
from typing import Dict, Any

from pydantic import Field

from bug_killer_utils.model.bk_base_model import BkBaseModel


class HttpStatusCodes(int, Enum):
    OK_STATUS = 200
    CREATED_STATUS = 201
    BAD_REQUEST_STATUS = 400
    UNAUTHORIZED_STATUS = 401
    FORBIDDEN_STATUS = 403
    NOT_FOUND_STATUS = 404
    INTERNAL_SERVER_ERROR_STATUS = 500


class HttpResponse(BkBaseModel):
    status_code: HttpStatusCodes
    headers: Dict[str, Any] = Field(default_factory=dict)
    body: Dict[str, Any] = Field(default_factory=dict)

    _DEFAULT_HEADERS = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True
    }

    def api_dict(self) -> Dict[str, Any]:
        data = super().api_dict()
        data['headers'] = {**data['headers'], **HttpResponse._DEFAULT_HEADERS}
        data['body'] = json.dumps(data['body'])

        return data


class OkResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.OK_STATUS, const=True)


class UpdatedResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.OK_STATUS, const=True)


class CreatedResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.CREATED_STATUS, const=True)


class DeletedResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.OK_STATUS, const=True)


class BadRequestResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.BAD_REQUEST_STATUS, const=True)


class UnAuthorizedResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.UNAUTHORIZED_STATUS, const=True)


class ForbiddenResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.FORBIDDEN_STATUS, const=True)


class NotFoundResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.NOT_FOUND_STATUS, const=True)


class InternalServerErrorResponse(HttpResponse):
    status_code = Field(HttpStatusCodes.INTERNAL_SERVER_ERROR_STATUS, const=True)


def message_body(message: str) -> Dict[str, Any]:
    return {'message': message}
