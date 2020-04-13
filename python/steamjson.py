import sys
import url
import json

class SteamJson:
    _STEAMAPI_BASE = ("http://api.steampowered.com/"
                      "/IDOTA2Match_570"
                      "/GetMatchHistory/v1")
    _STEAMAPI_LEAGUE = "?league_id="
    _STEAMAPI_KEY = "&key="
    _STEAMAPI_REQUEST = "&matches_requested="
    _STEAMAPI_MAXREQUEST = 300

    def __init__(self, leagueid, apikey):
        self.root = {}
        self._leagueid = leagueid
        self._apikey = apikey
        ####
        self.make_matchid_json()

    def make_matchid_json(self):
        has_next = True
        while(has_next):
            has_next = False
            result={}
            _url = (self._STEAMAPI_BASE
                    + self._STEAMAPI_LEAGUE
                    + str(self._leagueid)
                    + self._STEAMAPI_KEY
                    + str(self._apikey)
                    + self._STEAMAPI_REQUEST
                    + str(self._STEAMAPI_MAXREQUEST))
            result = url.get_url(_url)
            print(json.dumps(result, indent = 4))


if __name__ == "__main__":
    pass
