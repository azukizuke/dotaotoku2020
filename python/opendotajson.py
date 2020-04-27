import json
import url


class OpendotaJson:
    _OPENDOTAAPI_BASE = "https://api.opendota.com/api/matches/"
    _OPENDOTAAPI_KEY = "?api_key="
    _FILENAME_SUFFIX = "_opendotaapi.json"

    def __init__(self, leagueid, apikey, steamjson, indexjson):
        # init
        self._leagueid = leagueid
        self._apikey = apikey
        self._steamjson = steamjson
        self._indexjson = indexjson
        self.details = {}

        # make opendota json
        self._make_details()

    def _make_details(self):
        for matchid in self._steamjson.get_matches().keys():
            _url = self._make_url(matchid)
            result = url.get_url(_url)
            self._add_detail(result)

    def _make_url(self, matchid):
        url = (self._OPENDOTAAPI_BASE
               + str(matchid)
               + self._OPENDOTAAPI_KEY
               + str(self._apikey))
        return url

    def _add_detail(self, result):
        if result['game_mode'] == 2:
            self.details[result['match_id']] = result

    def write_json(self, folder_path):
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        with open(filepath, mode='w') as f:
            json.dump(self.details, f, indent=4)

    def get_details(self):
        return self.details

    def get_match_num(self):
        return len(self.details)

    def get_last_matchid(self):
        return (next(iter(self.details)))

    def get_last_unixdate(self):
        return (self._steamjson.get_last_unixdate())

    def get_leaguename(self):
        return (self.details[next(iter(self.details))]['league']['name'])

    def get_match_skillstats(self, matchid):
        skillstats = {}
        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            skillarr = player['ability_upgrades_arr']
            skillstats[heroid] = skillarr
        return skillstats

    def get_match_talentstats(self, matchid):
        talentstats = {}
        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            talentarr = []
            skillarr = player['ability_upgrades_arr']
            if not isinstance(skillarr, type(None)):
                for skill in skillarr:
                    if (self._indexjson.is_talent(str(skill))):
                        talentarr.append(skill)
                talentstats[heroid] = talentarr
        return talentstats

    def get_match_lastitems(self, matchid):
        lastitems = {}
        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            itemarr = []
            itemarr.append(player['item_0'])
            itemarr.append(player['item_1'])
            itemarr.append(player['item_2'])
            itemarr.append(player['item_3'])
            itemarr.append(player['item_4'])
            itemarr.append(player['item_5'])
            lastitems[heroid] = itemarr
        return lastitems

    def get_match_lastneutralitems(self, matchid):
        lastneutralitems = {}
        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            neutralitem = player['item_neutral']
            lastneutralitems[heroid] = neutralitem
        return lastneutralitems


if __name__ == '__main__':
    pass
