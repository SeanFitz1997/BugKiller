import json
import os.path
from typing import Optional, Dict


DEFAULT_DATA_PATH = os.path.join('data', 'cli_defaults.json')


def get_cli_defaults() -> Optional[Dict[str, str]]:
    if os.path.exists(DEFAULT_DATA_PATH):
        with open(DEFAULT_DATA_PATH) as f:
            defaults = json.load(f)
            return defaults
