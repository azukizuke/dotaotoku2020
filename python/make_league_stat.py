import sys
import json
import steamjson

if __name__ == "__main__":
    leagueid = sys.argv[1]
    apikey = sys.argv[2]

    print("--start--")
    steamjson = steamjson.SteamJson(leagueid, apikey)
    print(json.dumps(steamjson.matches, indent = 4))
    print("--end--")
