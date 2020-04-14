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
    apikey = sys.argv[2]

    print("--start--")
    # crate folder
    league_folder = PARENT_LEAGUE_FOLDER_PATH / leagueid
    league_folder.mkdir(exist_ok=True)

    # steam
    steamjson = steamjson.SteamJson(leagueid, apikey)
    steamjson.write_json(league_folder)

    # opendota

    # make stat

    # debug
    # print(json.dumps(steamjson.matches, indent = 4))
    print("--end--")
