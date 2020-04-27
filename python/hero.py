import re
import json
import traceback


class Hero:
    def __init__(self, heroid, name, indexjson):
        self.heroid = heroid
        self.name = name
        self._indexjson = indexjson
        self.pickbans = {}
        self.hero_role = {}
        self.ability_ids = []
        self.imagefile = ""
        # dict stats
        self.skillstats = {}
        self.talentstats = {}
        self.lastitems = {}
        self.lastneutralitems = {}
        # init function
        self._init_pickbans()
        self._init_role()
        self._init_skillstats()
        self._init_talentstats()
        self.imagefile = self._init_imagefile()

    def _init_imagefile(self):
        herojson = self._indexjson.opendota_heroes
        original_imagefile = herojson[self.heroid]['img']
        imagefile = original_imagefile.split('/')[-1].rstrip('?').split('.')[0]
        return imagefile

    def _init_pickbans(self):
        for k, v in self._indexjson.pickbans.items():
            self.pickbans[k] = 0

    def _init_skillstats(self):
        abilities = self._indexjson.opendota_hero_abilities
        ability_ids = self._indexjson.opendota_ability_ids

        for ability in abilities[self.name]['abilities']:
            ability_id = self._indexjson.get_ability_id(ability)
            self.ability_ids.append(ability_id)

        for value in abilities[self.name]['talents']:
            ability_id = self._indexjson.get_ability_id(value['name'])
            self.ability_ids.append(ability_id)

        for i in range(1, 26):
            skillstats = {}
            for abilityid in self.ability_ids:
                skillstats[abilityid] = 0
            self.skillstats[i] = skillstats

    def _init_talentstats(self):
        abilities = self._indexjson.opendota_hero_abilities
        ability_ids = self._indexjson.opendota_ability_ids
        for value in abilities[self.name]['talents']:
            ability_id = self._indexjson.get_ability_id(value['name'])
            level = value['level']
            if level in self.talentstats:
                self.talentstats[level][ability_id] = 0
            else:
                self.talentstats[level] = {ability_id: 0}

    def _init_role(self):
        for k, v in self._indexjson.role_index.items():
            self.hero_role[k] = self._indexjson.hero_role[self.heroid][k]

    def add_pickbans(self, order):
        # order
        self.pickbans[str(order)] += 1

        # all
        self.pickbans['all'] += 1

        # pick/ban
        if self._indexjson.pickbans[str(order)]['is_pick']:
            self.pickbans['pick'] += 1
        else:
            self.pickbans['ban'] += 1

        # type
        self.pickbans[self._indexjson.pickbans[str(order)]['type']] += 1

    def add_skillstats(self, skillarr):
        for i, skillid in enumerate(skillarr, 1):
            self.skillstats[i][str(skillid)] += 1

    def add_talentstats(self, talentarr):
        for talent in talentarr:
            for level, talents in self.talentstats.items():
                for _talent in talents:
                    if str(_talent) == str(talent):
                        self.talentstats[level][_talent] += 1

    def add_lastitems(self, lastitems):
        for item in lastitems:
            if item in self.lastitems:
                self.lastitems[item] += 1
            else:
                self.lastitems[item] = 1

    def add_lastneutralitems(self, neutralitems):
        for item in neutralitems:
            if item in self.lastneutralitems:
                self.lastneutralitems[item] += 1
            else:
                self.lastneutralitems[item] = 1

    def get_pickbans(self, order):
        return self.pickbans[str(order)]

    def make_herojson(self):
        output_dict = {}
        output_dict['heroid'] = self.heroid
        output_dict['name'] = self.name
        output_dict['pickbans'] = self.pickbans
        output_dict['skillstats'] = self.skillstats
        output_dict['talentstats'] = self.talentstats
        output_dict['lastitems'] = self.lastitems
        output_dict['lastneutralitems'] = self.lastneutralitems
        output_dict['hero_role'] = self.hero_role
        output_dict['imagefile'] = self.imagefile
        return output_dict
