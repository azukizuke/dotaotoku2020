import re
import copy
import json
import traceback


class Ability:
    def __init__(self, indexjson):
        # dict
        self._abilities_dict = {}
        self._indexjson = indexjson
        self._init_abilities_dict(self._indexjson.opendota_ability_ids,
                                  self._indexjson.opendota_abilities)

    def _init_abilities_dict(self, ability_ids, abilities):
        for ability_id, ability_name in ability_ids.items():
            self._abilities_dict[ability_id] = {'name': ability_name}
            self._abilities_dict[ability_id]['img'] = ability_name + '_lg'
            if (ability_name in abilities) and 'dname' in abilities[ability_name]:
                dname = abilities[ability_name]['dname']
            else:
                dname = ability_name
            self._abilities_dict[ability_id]['dname'] = dname


        ## talent id
        self._abilities_dict['-100'] = {
            'name' : 'talent',
            'dname' : 'talent',
            'img' : 'talent',
        }

    def make_json(self):
        return self._abilities_dict
