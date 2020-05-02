import re
import copy
import json
import traceback


class Ability:
    def __init__(self, indexjson):
        # dict
        self._abilities_dict = {}
        self._indexjson = indexjson
        self._init_abilities_dict(self._indexjson.opendota_ability_ids)

    def _init_abilities_dict(self, ability_ids):
        for ability_id, ability_name in ability_ids.items():
            self._abilities_dict[ability_id] = {'name': ability_name}
            self._abilities_dict[ability_id]['img'] = ability_name + '_lg'
        ## talent id
        self._abilities_dict['-100'] = {
            'name' : 'talent',
            'img' : 'talent',
        }

    def make_json(self):
        return self._abilities_dict
