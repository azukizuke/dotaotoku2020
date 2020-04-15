
class Hero:
    def __init__(self, heroid, name, indexjson):
        self.heroid = heroid
        self.name = name
        self._indexjson = indexjson
        self.pickbans = {}
        self._init_pickbans()

    def _init_pickbans(self):
        for k, v in self._indexjson.pickbans.items():
            self.pickbans[k] = 0

    def add_pickbans(self, order):
        self.pickbans[str(order)] += 1

    def get_pickbans(self, order):
        return self.pickbans[str(order)]
