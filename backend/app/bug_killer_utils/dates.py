from typing import Optional, Union

import arrow
from arrow import Arrow


def to_utc_str(dt: Arrow) -> str:
    return dt.format('YYYY-MM-DDTHH:mm:ss') + 'Z'


def try_parse_arrow(data: Optional[Union[str, Arrow]], is_optional: bool = False) -> Optional[Arrow]:
    if data and type(data) is str:
        return arrow.get(data)
    else:
        if not is_optional:
            raise ValueError(f'Failed to parse arrow object from {data = }')
        else:
            return None
