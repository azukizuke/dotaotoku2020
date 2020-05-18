import json
import url


class OpendotaJson:
    _OPENDOTAAPI_BASE = "https://api.opendota.com/api/matches/"
    _OPENDOTAAPI_KEY = "?api_key="
    _FILENAME_SUFFIX = "_opendotaapi.json"

    def __init__(self,
                 leagueid,
                 apikey,
                 steamjson,
                 indexjson,
                 folder_path,
                 is_matchlist_not_change):
        # init
        self._leagueid = leagueid
        self._apikey = apikey
        self._steamjson = steamjson
        self._indexjson = indexjson
        self.details = {}

        # make opendota json
        if is_matchlist_not_change:
            self.details = self.read_json(folder_path)
        else:
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

    def read_json(self, folder_path):
        details = {}
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        with open(filepath, mode='r') as f:
            details = json.load(f)
        return(details)

    def get_details(self):
        return self.details

    def get_match_num(self):
        return len(self.details)

    def get_radiant_win_num(self):
        radiant_win_num = 0
        for detail in self.details.values():
            if detail['radiant_win']:
                radiant_win_num += 1
        return radiant_win_num

    def get_last_matchid(self):
        return (next(iter(self.details)))

    def get_match_id_arr(self):
        match_id_arr = []
        for match_id in self.details.keys():
            match_id_arr.append(match_id)
        return match_id_arr

    def get_unixdate_arr(self):
        return (self._steamjson.get_unixdate_arr())

    def get_last_unixdate(self):
        return (self._steamjson.get_last_unixdate())

    def get_leaguename(self):
        detail = self.details[next(iter(self.details))]
        if 'league' in detail:
            return (self.details[next(iter(self.details))]['league']['name'])
        return self._leagueid

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

    def get_match_startitems(self, matchid):
        startitems = {}
        for player in self.details[matchid]['players']:
            startitem = []
            heroid = player['hero_id']
            purchaselog = player['purchase_log']
            if not isinstance(purchaselog, type(None)):
                for purchase in purchaselog:
                    if purchase['time'] <= 0:
                        itemid = self._indexjson.get_item_id(purchase['key'])
                        startitem.append(itemid)
                startitems[heroid] = sorted(startitem)
        return startitems

    def get_match_purchaselog(self, matchid):
        purchaselog = {}
        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            purchaselog[heroid] = player['purchase_log']
        return purchaselog

    def get_match_duration(self, matchid):
        duration = self.details[matchid]['duration']
        return duration

    def get_match_is_win(self, matchid):
        is_win = {}
        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            if player['win'] == 1:
                is_win[heroid] = True
            else:
                is_win[heroid] = False
        return is_win

    def _get_most_sentry(self, players):
        sentry_ranking = {}
        for player in players:
            heroid = player['hero_id']
            if 'purchase_ward_sentry' in player:
                sentry_ranking[heroid] = player['purchase_ward_sentry']
            else:
                sentry_ranking[heroid] = 0
        sorted_ranking = sorted(sentry_ranking.items(),
                                reverse=True,
                                key=lambda x: x[1])
        return sorted_ranking[0][0]

    def _get_supports(self, players):
        lasthit = {}
        for player in players:
            try:
                if not isinstance(player['lh_t'], type(None)):
                    heroid = player['hero_id']
                    lh = player['lh_t'][10]
                    lasthit[heroid] = lh
            except TypeError:
                print("---TypeError---")
                print("---player", player)
                print("---lh", player['lh_t'])
                raise

        sorted_ranking = sorted(lasthit.items(), key=lambda x: x[1])
        try:
            if len(sorted_ranking) == 0:
                return []
            return [sorted_ranking[0][0], sorted_ranking[1][0]]
        except IndexError:
            print("---IndexError")
            print("---sorted_ranking",sorted_ranking)
            raise

    def _get_teamplayers(self, players, isRadiant):
        team_players = []
        for player in players:
            if player['isRadiant'] == isRadiant:
                team_players.append(player)
        return team_players

    def _get_gold_ranking(self, players):
        networth = {}
        for player in players:
            if 'total_gold' in player:
                heroid = player['hero_id']
                gold = player['total_gold']
            networth[heroid] = gold
        sorted_ranking = sorted(networth.items(),
                                key=lambda x: x[1],
                                reverse=True)
        return sorted_ranking

    def get_match_autorole(self, matchid):
        autorole = {}

        radiant = self._get_teamplayers(self.details[matchid]['players'], True)
        dire = self._get_teamplayers(self.details[matchid]['players'], False)

        autorole[self._get_most_sentry(radiant)] = 'pos5'
        autorole[self._get_most_sentry(dire)] = 'pos5'

        supports = self._get_supports(radiant)
        supports.extend(self._get_supports(dire))

        for support in supports:
            if support not in autorole:
                autorole[support] = 'pos4'

        for player in self.details[matchid]['players']:
            heroid = player['hero_id']
            if (heroid not in autorole
               and 'lane_role' in player):
                if player['lane_role'] == 2:
                    autorole[heroid] = 'pos2'

        gold_ranking = []
        gold_ranking.append(self._get_gold_ranking(radiant))
        gold_ranking.append(self._get_gold_ranking(dire))

        for team in gold_ranking:
            has_pos1 = False
            for rank in team:
                if not rank[0] in autorole:
                    if has_pos1:
                        autorole[rank[0]] = 'pos3'
                    else:
                        autorole[rank[0]] = 'pos1'
                        has_pos1 = True
        return autorole


if __name__ == '__main__':
    pass
