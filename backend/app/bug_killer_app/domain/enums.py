from enum import Enum


class ResourceType(str, Enum):
    """ Names of resources in the Bk Domain """
    PROJECT = 'project'
    BUG = 'bug'
    MANAGER = 'manager'


class ParameterType(str, Enum):
    """ Names API request parameter types """
    BODY = 'body'
    HEADERS = 'headers'
    PATH = 'pathParameters'
    QUERY = 'queryStringParameters'
    CONTEXT = 'requestContext'
