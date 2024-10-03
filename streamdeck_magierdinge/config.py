import os.path
import tomllib
from pathlib import Path
from box import Box


CONFIG_PATHS = [
    '.env.toml'
]


def load_config() -> Box:
    for path in CONFIG_PATHS:
        try:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    config = Box(tomllib.load(f))
                    return config
        except IOError as e:
            continue
    return Box()


