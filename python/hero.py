class Hero:
    def __init__(self, heroid, name, indexjson):
        # other class
        self._indexjson = indexjson
        # single info
        self.heroid = heroid
        self.name = name
        self.imagefile = ""
        self.localized_name = (self._indexjson.
                               opendota_heroes[self.heroid]['localized_name'])
        # single stats
        self.win_stats = 0
        # dict info
        self.hero_role = {}
        self.ability_ids = []
        self.talent_ids = {}
        # dict stats
        self.pickbans = {}
        self.ability_ids_order = {}
        # dict stats
        self.skillstats = {}
        self.skill_stats_fix = {}
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
        for k in self._indexjson.pickbans.keys():
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

    def init_skill_stats_fix(self):
        for abilityid in self.ability_ids:
            init_dict = {}
            for level in range(1, 26):
                init_dict[level] = 0
            self.skill_stats_fix[abilityid] = init_dict
        # init talent id
        init_dict = {}
        for level in range(1, 26):
            init_dict[level] = 0
        self.skill_stats_fix['-100'] = init_dict

    def init_ability_ids(self):
        abilities = self._indexjson.opendota_hero_abilities
        for ability in abilities[self.name]['abilities']:
            ability_id = self._indexjson.get_ability_id(ability)
            self.ability_ids.append(ability_id)
        for value in abilities[self.name]['talents']:
            ability_id = self._indexjson.get_ability_id(value['name'])
            self.ability_ids.append(ability_id)
        # make order for favascript
        self.init_ability_ids_order()

    def init_ability_ids_order(self):
        for order, ability_id in enumerate(self.ability_ids):
            # ignore blank skill id or talent id
            if ability_id != '6251':
                # ignore talent id
                if not self._indexjson.is_talent(ability_id):
                    self.ability_ids_order[order] = ability_id
        self.ability_ids_order[99999] = '-100'

    def delete_unselect_ability_order(self):
        if self.pickbans['pick'] > 0:
            delete_order_arr = []
            for ability_id, count_arr in self.skill_stats_fix.items():
                count_sum = 0
                for count in count_arr.values():
                    count_sum += count
                if count_sum == 0:
                    for order, order_ability_id in self.ability_ids_order.items():
                        if str(ability_id) == str(order_ability_id):
                            delete_order_arr.append(order)
            for order in delete_order_arr:
                self.ability_ids_order.pop(order)

    def init_talent_ids(self):
        abilities = self._indexjson.opendota_hero_abilities
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
        for k in self._indexjson.role_index.keys():
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

    def add_skill_stats_fix(self, skill_arr):
        for i, skill_id in enumerate(skill_arr, 1):
            self.skill_stats_fix[str(skill_id)][i] += 1
            if self._indexjson.is_talent(skill_id):
                self.skill_stats_fix['-100'][i] += 1

    def add_talentstats(self, talentarr):
        for talent in talentarr:
            for level, talents in self.talentstats.items():
                for _talent in talents:
                    if str(_talent) == str(talent):
                        self.talentstats[level][_talent] += 1

    def add_lastitems(self, lastitems):
        for item in lastitems:
            if item != 0:
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
        i = 0
        index_json = self._indexjson
        for purchase in purchaselog:
            if purchase['time'] >= 0:
                item = self._indexjson.get_item_id(purchase['key'])
                item_cost = self._indexjson.get_item_cost(purchase['key'])
                is_created = self._indexjson.is_item_created(purchase['key'])
                is_consumable = index_json.is_item_consumable(purchase['key'])
                if (not is_consumable):
                    if not ((not is_created) and item_cost < 620):
                        if i in self.purchasestats:
                            if item in self.purchasestats[i]:
                                self.purchasestats[i][item] += 1
                            else:
                                self.purchasestats[i][item] = 1
                        else:
                            self.purchasestats[i] = {item: 1}
                        i += 1

    def add_lastneutralitems(self, neutral_item):
        if neutral_item != 0:
            if neutral_item in self.lastneutralitems:
                self.lastneutralitems[neutral_item] += 1
            else:
                self.lastneutralitems[neutral_item] = 1

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
        output_dict['ability_ids_order'] = self.ability_ids_order
        output_dict['talent_ids'] = self.talent_ids
        output_dict['hero_role'] = self.hero_role
        # multi stats
        output_dict['pickbans'] = self.pickbans
        output_dict['skillstats'] = self.skillstats
        output_dict['skill_stats_fix'] = self.skill_stats_fix
        output_dict['talentstats'] = self.talentstats
        output_dict['lastitems'] = self.lastitems
        output_dict['start_item_stats'] = self.startitemstats
        output_dict['purchasestats'] = self.purchasestats
        output_dict['lastneutralitems'] = self.lastneutralitems
        return output_dict
