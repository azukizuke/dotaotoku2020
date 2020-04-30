import re
import copy
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
        self.talent_ids = {}
        self.imagefile = ""
        # single info
        self.localized_name = self._indexjson.opendota_heroes[self.heroid]['localized_name']
        # single stats
        self.win_stats = 0
        # dict stats
        self.skillstats = {}
        self.talentstats = {}
        self.lastitems = {}
        self.lastneutralitems = {}
        self.startitemstats = []
        self.purchasestats = {}
        # init function
        self._init_pickbans()
        self._init_role()
        self.imagefile = self._init_imagefile()
        # skill init timing is after
        self.init_ability_ids()
        self.init_talent_ids()
        # stats init from league Class. after add skill
        # self.init_skillstats()
        # self.init_talentstats()

    def _init_imagefile(self):
        herojson = self._indexjson.opendota_heroes
        original_imagefile = herojson[self.heroid]['img']
        imagefile = original_imagefile.split('/')[-1].rstrip('?').split('.')[0]
        return imagefile

    def _init_pickbans(self):
        for k, v in self._indexjson.pickbans.items():
            self.pickbans[k] = 0

    def add_abilities(self, ability_upgrades_arr):
        for ability_id in ability_upgrades_arr:
            if str(ability_id) not in self.ability_ids:
                self.ability_ids.append(str(ability_id))

    def add_talent_ids(self, talent_arr):
        for i, talent_id in enumerate(talent_arr, 1):
            if i <= 4:
                if str(talent_id) not in self.talent_ids[i]:
                    self.talent_ids[i].append(str(talent_id))

    def init_skillstats(self):
        for i in range(1, 26):
            skillstats = {}
            for abilityid in self.ability_ids:
                skillstats[abilityid] = 0
            self.skillstats[i] = skillstats

    def init_ability_ids(self):
        abilities = self._indexjson.opendota_hero_abilities
        ability_ids = self._indexjson.opendota_ability_ids
        for ability in abilities[self.name]['abilities']:
            ability_id = self._indexjson.get_ability_id(ability)
            self.ability_ids.append(ability_id)
        for value in abilities[self.name]['talents']:
            ability_id = self._indexjson.get_ability_id(value['name'])
            self.ability_ids.append(ability_id)

    def init_talent_ids(self):
        abilities = self._indexjson.opendota_hero_abilities
        ability_ids = self._indexjson.opendota_ability_ids
        for value in abilities[self.name]['talents']:
            ability_id = self._indexjson.get_ability_id(value['name'])
            level = value['level']
            if level in self.talent_ids:
                self.talent_ids[level].append(ability_id)
            else:
                self.talent_ids[level] = [ability_id]

    def init_talentstats(self):
        for level, talent_id_arr in self.talent_ids.items():
            for talent_id in talent_id_arr:
                if level in self.talentstats:
                    self.talentstats[level][talent_id] = 0
                else:
                    self.talentstats[level] = {talent_id: 0}

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

    def add_startitems(self, startitems):
        # startitems count
        has_item = -1
        for i, items in enumerate(self.startitemstats):
            if items['startitems'] == startitems:
                has_item = i

        if has_item == -1:
            self.startitemstats.append({'startitems': startitems, 'count': 1})
        else:
            self.startitemstats[has_item]['count'] += 1

    def add_autoroles(self, autorole):
        self.pickbans[autorole] += 1

    def add_purchaselog(self, purchaselog):
        for i, purchase in enumerate(purchaselog):
            item = self._indexjson.get_item_id(purchase['key'])
            if i in self.purchasestats:
                if item in self.purchasestats[i]:
                    self.purchasestats[i][item] += 1
                else:
                    self.purchasestats[i][item] = 1
            else:
                self.purchasestats[i] = {item: 1}

    def add_lastneutralitems(self, neutralitems):
        for item in neutralitems:
            if item in self.lastneutralitems:
                self.lastneutralitems[item] += 1
            else:
                self.lastneutralitems[item] = 1

    def get_pickbans(self, order):
        return self.pickbans[str(order)]

    def add_win_stats(self, is_win):
        if is_win:
            self.win_stats += 1

    def make_herojson(self):
        output_dict = {}
        # single info
        output_dict['heroid'] = self.heroid
        output_dict['name'] = self.name
        output_dict['localized_name'] = self.localized_name
        output_dict['imagefile'] = self.imagefile
        # single stats
        output_dict['win_stats'] = self.win_stats
        # multi info
        output_dict['ability_ids'] = self.ability_ids
        output_dict['talent_ids'] = self.talent_ids
        output_dict['hero_role'] = self.hero_role
        # multi stats
        output_dict['pickbans'] = self.pickbans
        output_dict['skillstats'] = self.skillstats
        output_dict['talentstats'] = self.talentstats
        output_dict['lastitems'] = self.lastitems
        output_dict['startitemistats'] = self.startitemstats
        output_dict['purchasestats'] = self.purchasestats
        output_dict['lastneutralitems'] = self.lastneutralitems
        return output_dict
