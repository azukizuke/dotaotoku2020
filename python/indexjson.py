import json
import re
import traceback
from pathlib import Path


class IndexJson:
    # opendota
    _OPENDOTA_HERO = "heroes.json"
    _OPENDOTA_HERO_ABILITIES = "hero_abilities.json"
    _OPENDOTA_ABILITY_IDS = "ability_ids.json"
    _OPENDOTA_ABILITIES = "abilities.json"
    _OPENDOTA_ITEM_IDS = "item_ids.json"
    # self
    _PICKBANS = "pickbans.json"
    _HERO_ROLE = "hero_role.json"
    _ROLE_INDEX = "role_index.json"

    def __init__(self, path_index, path_opendota_index):
        # opendota
        self.opendota_heroes = self._load_json(path_opendota_index
                                               / self._OPENDOTA_HERO)
        self.opendota_hero_abilities = self._load_json(
                                       path_opendota_index
                                       / self._OPENDOTA_HERO_ABILITIES)
        self.opendota_ability_ids = self._load_json(
                                    path_opendota_index
                                    / self._OPENDOTA_ABILITY_IDS)
        self.opendota_abilities = self._load_json(
                                  path_opendota_index
                                  / self._OPENDOTA_ABILITIES)
        self.opendota_item_ids = self._load_json(
                                 path_opendota_index
                                 / self._OPENDOTA_ITEM_IDS)
        # original
        self.pickbans = self._load_json(path_index/self._PICKBANS)
        self.hero_role = self._load_json(path_index/self._HERO_ROLE)
        self.role_index = self._load_json(path_index/self._ROLE_INDEX)

    def _load_json(self, path):
        with open(path) as f:
            result = json.load(f)
        return result

    def get_ability_id(self, abilityname):
        for abilityid, ability in self.opendota_ability_ids.items():
            if abilityname == ability:
                return(abilityid)

    def get_item_id(self, item):
        for itemid, itemname in self.opendota_item_ids.items():
            if item == itemname:
                return(itemid)

    def get_ability_name(self, abilityid):
        for _abilityid, _ability in self.opendota_ability_ids.items():
            if str(abilityid) == str(_abilityid):
                return(_ability)

    def is_talent(self, abilityid):
        abilityname = self.get_ability_name(abilityid)
        try:
            if re.match(r'^special_bonus_.*', abilityname):
                return True
            else:
                return False
        except TypeError:
            print("---TyperError---")
            traceback.print_exc()
            print("---")
            print("abilityname: ",abilityname)
            print("abilityid: ",abilityid)
            print("---")
            raise

