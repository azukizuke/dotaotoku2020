import sys
import json
from pathlib import Path
import steamjson
import opendotajson

# CONST
PARENT_LEAGUE_FOLDER = "leaguedata"
PARENT_LEAGUE_FOLDER_PATH = (Path(__file__).resolve().parent.parent
                             / PARENT_LEAGUE_FOLDER)

# MAIN
if __name__ == "__main__":
    leagueid = sys.argv[1]
    apikey_steam = sys.argv[2]
    apikey_opendota = sys.argv[3]
    startid = sys.argv[4]

    print("--start--")
    # crate folder
    league_folder = PARENT_LEAGUE_FOLDER_PATH / leagueid
    league_folder.mkdir(exist_ok=True)

    # steam
    steamjson = steamjson.SteamJson(leagueid, apikey_steam, startid)
    steamjson.write_json(league_folder)

    # opendota
    opendotajson = opendotajson.OpendotaJson(leagueid,
                                             apikey_opendota,
                                             steamjson)
    opendotajson.write_json(league_folder)

    # make stat

    # debug
    # print(json.dumps(steamjson.matches, indent = 4))
    print("--end--")
