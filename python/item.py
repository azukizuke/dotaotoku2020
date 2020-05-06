import re
import copy
import json
import traceback


class Item:
    def __init__(self, indexjson):
        self._item_dict = {}
        self._indexjson = indexjson
        self._init_item_dict(self._indexjson.opendota_item_ids)

    def _init_item_dict(self, opendota_item_ids):
        for item_id, item_name in opendota_item_ids.items():
            self._item_dict[item_id] = {'name': item_name}
            self._item_dict[item_id]['img'] = item_name + "_lg"

    def make_json(self):
        return self._item_dict
