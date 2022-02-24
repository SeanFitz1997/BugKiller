import re
from typing import List, Optional


def snake_case_to_camel_case(x: str) -> str:
    words = x.split('_')
    if len(words) < 2:
        return x
    words = words[:1] + [capitalize(word) for word in words[1:]]
    return ''.join(words)


def camel_case_to_snake_case(x: str) -> str:
    return ''.join(['_' + char.lower() if char.isupper() else char for char in x]).lstrip('_')


def capitalize(x: str) -> str:
    if len(x) > 0:
        capital_char = x[0].upper()
        return capital_char + x[1:]
    else:
        return x


def find_all_text_in_single_quotes(text: str) -> List[str]:
    return re.findall(r"'([^']*)'", text)


def remove_prefix(prefix: str, string: str) -> str:
    return string.split(prefix, maxsplit=1)[-1]


def is_blank(x: Optional[str]) -> bool:
    return not x or not x.strip()
