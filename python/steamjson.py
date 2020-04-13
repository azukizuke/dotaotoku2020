import sys


class SteamJson:

    def __init__(self, leagueid, apikey):
        self.root = {}
        self._leagueid = leagueid
        self._apikey = apikey
        ####
        self.make_matchid_json()

    def make_matchid_json(self):
        has_next = False
        while(not has_next):
            print("test")
            has_next = True


if __name__ == "__main__":
    pass
