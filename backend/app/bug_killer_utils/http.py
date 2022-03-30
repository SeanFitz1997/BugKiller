from enum import Enum


class HttpMethod(str, Enum):
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'
    DELETE = 'delete'


class HttpStatusCode(int, Enum):
    OK_STATUS = 200
    CREATED_STATUS = 201
    BAD_REQUEST_STATUS = 400
    UNAUTHORIZED_STATUS = 401
    FORBIDDEN_STATUS = 403
    NOT_FOUND_STATUS = 404
    INTERNAL_SERVER_ERROR_STATUS = 500
