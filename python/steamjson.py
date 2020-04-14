import sys
import url
import json
import copy


class SteamJson:
    _STEAMAPI_BASE = ("http://api.steampowered.com/"
                      "/IDOTA2Match_570"
                      "/GetMatchHistory/v1")
    _STEAMAPI_LEAGUE = "?league_id="
    _STEAMAPI_KEY = "&key="
    _STEAMAPI_REQUEST = "&matches_requested="
    _STEAMAPI_MAXREQUEST = 300
    _STEAMAPI_STARTID = "&start_at_match_id="

    def __init__(self, leagueid, apikey):
        self.matches = {}
        self._leagueid = leagueid
        self._apikey = apikey
        ####
        self.make_matchid_json()

    def make_matchid_json(self):
        is_first = True
        start_id = -1
        while(True):
            has_next = False
            result = {}
            _url = self._make_steam_url(start_id)
            result = url.get_url(_url)
            sort_matches = self._sort_matches_api(result)

            if not self._has_next(sort_matches):
                break

            self._add_match(sort_matches)
            start_id = sort_matches[-1]['match_id']

    def _make_steam_url(self, start_id=-1):
        url = (self._STEAMAPI_BASE
               + self._STEAMAPI_LEAGUE
               + str(self._leagueid)
               + self._STEAMAPI_KEY
               + str(self._apikey)
               + self._STEAMAPI_REQUEST
               + str(self._STEAMAPI_MAXREQUEST))
        if start_id != -1:
            url += (self._STEAMAPI_STARTID
                    + str(start_id))
        return(url)

    def _sort_matches_api(self, result):
        sort_matches = (sorted(result['result']['matches'],
                        key=lambda x: x['match_id'],
                        reverse=True))
        return(sort_matches)

    def _has_next(self, matches):
        if len(matches) < 1:
            return False
        else:
            return True

    def _add_match(self, matches):
        for match in matches:
            if match['lobby_type'] == 1:
                self.matches[match['match_id']] = copy.deepcopy(match)
        pass


if __name__ == "__main__":
    pass
