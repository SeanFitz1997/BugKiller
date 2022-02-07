from typing import Optional, Union

import arrow
import pytest
from arrow import Arrow

from bug_killer_utils.dates import to_utc_str


@pytest.mark.parametrize('dt, expected', [
    (arrow.get('2022-01-01'), '2022-01-01T00:00:00Z'),
    (arrow.get('2022-01-01').replace(tzinfo='US/Pacific'), '2022-01-01T08:00:00Z')
])
def test_to_utc_str(dt, expected):
    assert to_utc_str(dt) == expected


@pytest.mark.parametrize('dt, is_optional, expected', [
    (arrow.get('2022-01-01'), False, arrow.get('2022-01-01')),
    ('2022-01-01', False, arrow.get('2022-01-01')),
    (None, True, None)
])
def test_try_parse_arrow(dt, is_optional, expected):
    assert try_parse_arrow(dt, is_optional) == expected


def test_try_parse_arrow_missing_required_dt():
    with pytest.raises(ValueError):
        try_parse_arrow(None, is_optional=False)


def try_parse_arrow(data: Optional[Union[str, Arrow]], is_optional: bool = False) -> Optional[Arrow]:
    if isinstance(data, str):
        return arrow.get(data)
    elif isinstance(data, Arrow):
        return data
    else:
        if not is_optional:
            raise ValueError(f'Failed to parse arrow object from {data = }')
        else:
            return None
