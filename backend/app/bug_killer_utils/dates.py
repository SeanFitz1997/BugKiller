from typing import Optional, Union

import arrow
from arrow import Arrow
from dateutil.tz import tzutc


def to_utc_str(dt: Arrow) -> str:
    return dt.to('UTC').format('YYYY-MM-DDTHH:mm:ss') + 'Z'


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


def is_arrow_utc(dt: Arrow) -> bool:
    return type(dt.tzinfo) is tzutc
