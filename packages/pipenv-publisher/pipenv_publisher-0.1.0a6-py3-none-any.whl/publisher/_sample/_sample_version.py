import json
from pathlib import Path

with open(Path(__file__).parent.joinpath('meta.json')) as f:
    __meta_json__ = json.load(f)
    __version__ = __meta_json__['v']
    __author__ = __meta_json__['a']
    # https://stackoverflow.com/a/21356350/9256726 and https://stackoverflow.com/a/24293364/9256726
