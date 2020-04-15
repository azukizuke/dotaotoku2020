import hero
import json


class League:
    def __init__(self, leagueid, name, opendotajson, indexjson):
        # init
        self._leagueid = leagueid
        self._name = name
        self._opendotajson = opendotajson
        self._indexjson = indexjson
        self._herojson = {}

        # init hero
        self._init_herojson()

        # make stats
        self._make_stats()

    def _make_stats(self):
        for k,v in self._opendotajson.get_details().items():
            print(k)

    def _init_herojson(self):
        for k,v in self._indexjson.opendota_heroes.items():
            self._herojson[k] = hero.Hero(k, v['name'])
