import json
from typing import Dict, Any, Optional

from pydantic import Field

from bug_killer_utils.http import HttpStatusCode
from bug_killer_utils.model.bk_base_model import BkBaseModel


class HttpResponse(BkBaseModel):
    status_code: HttpStatusCode
    headers: Dict[str, Any] = Field(default_factory=dict)
    body: Dict[str, Any] = Field(default_factory=dict)

    _DEFAULT_HEADERS = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True,
    }

    def api_dict(self) -> Dict[str, Any]:
        data = super().api_dict()
        data['headers'] = {**data['headers'], **HttpResponse._DEFAULT_HEADERS}
        data['body'] = json.dumps(data['body'])

        return data

    @classmethod
    def test_double(  # type: ignore[override]
            cls, *,
            status_code: Optional[HttpStatusCode] = None,
            headers: Optional[Dict[str, Any]] = None,
            body: Optional[Dict[str, Any]] = None
    ) -> 'HttpResponse':
        return cls(
            status_code=status_code or HttpStatusCode.OK_STATUS,
            headers=headers or {},
            body=body or {'foo': 'bar'}
        )


def message_body(message: str) -> Dict[str, Any]:
    return {'message': message}
