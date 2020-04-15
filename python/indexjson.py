import json
from pathlib import Path


class IndexJson:
    _OPENDOTA_HERO = "heroes.json"
    _PICKBANS = "pickbans.json"

    def __init__(self, path_index, path_opendota_index):
        # opendota
        self.opendota_heroes = self._load_json(path_opendota_index
                                               / self._OPENDOTA_HERO)
        # original
        self.pickbans = self._load_json(path_index/self._PICKBANS)

    def _load_json(self, path):
        with open(path) as f:
            result = json.load(f)
        return result
