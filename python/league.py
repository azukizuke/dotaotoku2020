import hero
import json
import datetime
import traceback


class League:
    _FILENAME_SUFFIX = "_league.json"

    def __init__(self, leagueid, opendotajson, indexjson):
        # init
        self._leagueid = leagueid
        # self._name = name
        # self._year = year
        self._opendotajson = opendotajson
        self._indexjson = indexjson
        self._herojson = {}
        # init league stats
        self._match_num = self._opendotajson.get_match_num()
        self._last_matchid = self._opendotajson.get_last_matchid()
        self._last_unixdate = self._opendotajson.get_last_unixdate()
        self._name = self._opendotajson.get_leaguename()
        self._year = self._make_year_from_lastdate()
        self._pickbans = {}
        self._pickbans_ranking = {}
        self.leaguejson = {}

        # init dictionary
        self._init_herojson()

        # make stats
        self._make_stats()

    def _make_stats(self):
        # match rootin
        # init add skill/talent
        for match_id, v in self._opendotajson.get_details().items():
            self._init_hero_skill_stats(match_id)
            self._init_hero_talent_stats(match_id)
        # init allhero skill/talent stats
        for heroid, hero in self._herojson.items():
            hero.init_skillstats()
            hero.init_talentstats()

        # add
        for k, v in self._opendotajson.get_details().items():
            self._add_hero_pickbans(v['picks_bans'])
            self._add_hero_autoroles(k)
            self._add_hero_skillstats(k)
            self._add_hero_talentstats(k)
            self._add_hero_lastitems(k)
            self._add_hero_purchaselog(k)
            self._add_hero_startitems(k)
            self._add_hero_lastneutralitems(k)
            self._add_hero_is_win(k)

        # end of match rootin
        self._make_league_pickbans()

        # make_output_json
        self._make_leaguejson()
        self._make_herojson()

    def _make_league_pickbans(self):
        # order rootin
        for k, v in self._indexjson.pickbans.items():
            self._make_order_pickbans(k)

    def _make_order_pickbans(self, order):
        pickbans = {}
        for heroid, hero in self._herojson.items():
            pickbans[str(heroid)] = hero.get_pickbans(order)
        self._pickbans[str(order)] = pickbans

    def _init_hero_skill_stats(self, match_id):
        skill_stats = self._opendotajson.get_match_skillstats(match_id)
        for heroid, skill_arr in skill_stats.items():
            if (not isinstance(skill_arr, type(None))):
                self._herojson[str(heroid)].add_abilities(skill_arr)

    def _init_hero_talent_stats(self, match_id):
        talent_stats = self._opendotajson.get_match_talentstats(match_id)
        for heroid, talent_arr in talent_stats.items():
            if (not isinstance(talent_arr, type(None))):
                self._herojson[str(heroid)].add_talent_ids(talent_arr)

    def _add_hero_pickbans(self, pickbans):
        for v in pickbans:
            self._herojson[str(v['hero_id'])].add_pickbans(v['order'])

    def _add_hero_autoroles(self, matchid):
        autoroles = self._opendotajson.get_match_autorole(matchid)
        for heroid, autorole in autoroles.items():
            self._herojson[str(heroid)].add_autoroles(autorole)

    def _add_hero_skillstats(self, matchid):
        try:
            skillstats = self._opendotajson.get_match_skillstats(matchid)
            for heroid, skillarr in skillstats.items():
                if (not isinstance(skillarr, type(None))):
                    self._herojson[str(heroid)].add_skillstats(skillarr)
        except TypeError:
            traceback.print_exc()
            print("---error add hero skillstat-----------------")
            print("error matchid: ", matchid)
            print("error : heroid", heroid)
            print("error : skillstats", skillstats)
            raise

    def _add_hero_talentstats(self, matchid):
        talentstats = self._opendotajson.get_match_talentstats(matchid)
        if (not isinstance(talentstats, type(None))):
            for heroid, talentarr in talentstats.items():
                self._herojson[str(heroid)].add_talentstats(talentarr)

    def _add_hero_lastitems(self, matchid):
        lastitems = self._opendotajson.get_match_lastitems(matchid)
        for heroid, itemarr in lastitems.items():
            self._herojson[str(heroid)].add_lastitems(lastitems)

    def _add_hero_startitems(self, matchid):
        startitems = self._opendotajson.get_match_startitems(matchid)
        for heroid, startitem in startitems.items():
            self._herojson[str(heroid)].add_startitems(startitem)

    def _add_hero_lastneutralitems(self, matchid):
        opendotajson = self._opendotajson
        lastneutralitems = opendotajson.get_match_lastneutralitems(matchid)
        for heroid, newutralitems in lastneutralitems.items():
            self._herojson[str(heroid)].add_lastneutralitems(lastneutralitems)

    def _add_hero_is_win(self, matchid):
        is_win_dict = self._opendotajson.get_match_is_win(matchid)
        for heroid, is_win in is_win_dict.items():
            self._herojson[str(heroid)].add_win_stats(is_win)

    def _add_hero_purchaselog(self, matchid):
        purchaselog = self._opendotajson.get_match_purchaselog(matchid)
        for heroid, purchase in purchaselog.items():
            self._herojson[str(heroid)].add_purchaselog(purchase)

    def _init_herojson(self):
        for k, v in self._indexjson.opendota_heroes.items():
            self._herojson[k] = hero.Hero(k, v['name'], self._indexjson)

    def _make_leaguejson(self):
        self.leaguejson['name'] = self._name
        self.leaguejson['match_num'] = self._match_num
        self.leaguejson['year'] = self._year
        self.leaguejson['last_matchid'] = self._last_matchid
        self.leaguejson['last_unixdate'] = self._last_unixdate
        self.leaguejson['pickbans'] = self._pickbans

    def _make_herojson(self):
        self.leaguejson['heroes'] = {}
        for heroid, hero in self._herojson.items():
            self.leaguejson['heroes'][heroid] = hero.make_herojson()

    def write_json(self, folder_path):
        filename = str(self._leagueid) + self._FILENAME_SUFFIX
        filepath = folder_path / filename
        with open(filepath, mode='w') as f:
            json.dump(self.leaguejson, f, indent=4)

    def get_leaguejson(self):
        return self.leaguejson

    def _make_year_from_lastdate(self):
        # self._last_unixdate
        lastdate = datetime.datetime.fromtimestamp(self._last_unixdate)
        return (lastdate.year)
