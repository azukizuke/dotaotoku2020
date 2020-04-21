import json
from pathlib import Path


class IndexJson:
    _OPENDOTA_HERO = "heroes.json"
    _PICKBANS = "pickbans.json"
    _HERO_ROLE = "hero_role.json"
    _ROLE_INDEX = "role_index.json"

    def __init__(self, path_index, path_opendota_index):
        # opendota
        self.opendota_heroes = self._load_json(path_opendota_index
                                               / self._OPENDOTA_HERO)
        # original
        self.pickbans = self._load_json(path_index/self._PICKBANS)
        self.hero_role = self._load_json(path_index/self._HERO_ROLE)
        self.role_index = self._load_json(path_index/self._ROLE_INDEX)

    def _load_json(self, path):
        with open(path) as f:
            result = json.load(f)
        return result
