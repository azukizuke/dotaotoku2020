import json
from pathlib import Path

class IndexJson:
    _OPENDOTA_HERO = "heroes.json"
    def __init__(self, path_index, path_opendota_index):
        self.opendota_heroes = self._load_json(path_opendota_index/self._OPENDOTA_HERO)

    def _load_json(self, path):
        with open(path) as f:
            result = json.load(f)

        return result
