import re
from enum import Enum
from typing import Optional, List, Any

from pydantic import validator, Field

from bug_killer_utils.model.bk_base_model import BkBaseModel


class ParamTypes(str, Enum):
    HEADER = 'header'
    COOKIE = 'cookie'
    PATH = 'path'
    QUERY = 'query'


class ArgDetails(BkBaseModel):
    name: str
    description: str
    is_required: bool = True

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            name: Optional[str] = None,
            description: Optional[str] = None,
            is_required: bool = True
    ) -> 'BkBaseModel':
        return cls(
            name=name or 'test',
            description=description or 'A test value',
            is_required=is_required
        )


class PathDetails(BkBaseModel):
    path: str
    path_params: list[ArgDetails] = Field(default_factory=list)
    query_params: list[ArgDetails] = Field(default_factory=list)

    @validator('path_params')
    def validate_path_args(cls, value: List[ArgDetails], values: dict[str, Any]) -> Optional[list[ArgDetails]]:
        """ TODO """
        if value:
            args_in_path = set(re.findall(r'\{(.*?)}', values['path']))
            args_in_params = set(arg.name for arg in value)

            if not args_in_params == args_in_path:
                arg_diff = args_in_path.symmetric_difference(args_in_params)
                raise ValueError(f'The parameters in the path and params do not match. {arg_diff = }')

        return value

    @validator('path_params')
    def validate_query_args(cls, value: List[ArgDetails]) -> Optional[List[ArgDetails]]:
        """ TODO """
        return value

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            path: Optional[str] = None,
            args: Optional[List[ArgDetails]] = None
    ) -> 'PathDetails':
        return cls(
            path=path or '/test/{testId}',
            args=[ArgDetails.test_double(name='testId')]
        )
