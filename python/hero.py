import re


class Hero:
    def __init__(self, heroid, name, indexjson):
        self.heroid = heroid
        self.name = name
        self._indexjson = indexjson
        self.pickbans = {}
        self.hero_role = {}
        self.imagefile = ""
        # init function
        self._init_pickbans()
        self._init_role()
        self.imagefile = self._init_imagefile()

    def _init_imagefile(self):
        original_imagefile = self._indexjson.opendota_heroes[self.heroid]['img']
        imagefile = original_imagefile.split('/')[-1].rstrip('?').split('.')[0]
        return imagefile


    def _init_pickbans(self):
        for k, v in self._indexjson.pickbans.items():
            self.pickbans[k] = 0

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

    def get_pickbans(self, order):
        return self.pickbans[str(order)]

    def make_herojson(self):
        output_dict = {}
        output_dict['heroid'] = self.heroid
        output_dict['name'] = self.name
        output_dict['pickbans'] = self.pickbans
        output_dict['hero_role'] = self.hero_role
        output_dict['imagefile'] = self.imagefile
        return output_dict;
