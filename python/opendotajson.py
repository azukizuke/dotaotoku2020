import json
import url


class OpendotaJson:
    _OPENDOTAAPI_BASE = "https://api.opendota.com/api/matches/"
    _OPENDOTAAPI_KEY = "?api_key="
    _FILENAME_SUFFIX = "_opendotaapi.json"

    def __init__(self, leagueid, apikey, steamjson):
        # init
        self._leagueid = leagueid
        self._apikey = apikey
        self._steamjson = steamjson
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



if __name__ == '__main__':
    pass
