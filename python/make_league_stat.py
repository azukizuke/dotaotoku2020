import sys
import json
from pathlib import Path
import steamjson
import opendotajson
import indexjson
import league
import hero

# CONST
PARENT_LEAGUE_FOLDER = "leaguedata"
PARENT_LEAGUE_FOLDER_PATH = (Path(__file__).resolve().parent.parent
                             / PARENT_LEAGUE_FOLDER)
INDEX_JSON_FOLDER = "indexjson"
INDEX_JSON_FOLDER_PATH = (Path(__file__).resolve().parent.parent
                          / INDEX_JSON_FOLDER)
OPENDOTA_INDEX_JSON_FOLDER = "opendota-indexjson"
OPENDOTA_INDEX_JSON_FOLDER_PATH = (Path(__file__).resolve().parent.parent
                                   / OPENDOTA_INDEX_JSON_FOLDER)
ALL_LEAGUE_JSON_FILENAME = "allleague.json"

# Contoll all league data
def read_all_league_json(folderpath, filename):
    json_load = {}
    try:
        with open(folderpath / filename) as f:
            json_load = json.load(f)
        return json_load
    except FileNotFoundError:
        print("no all league file make new")
        return {}
    except json.decoder.JSONDecodeError:
        print("file is broken")
        return {}

def write_all_league_json(folderpath, filename, write_json):
    with open((folderpath / filename), mode='w') as f:
        json.dump(write_json, f, indent=4)

# MAIN
if __name__ == "__main__":
    # init
    leagueid = sys.argv[1]
    apikey_steam = sys.argv[2]
    apikey_opendota = sys.argv[3]
    startid = sys.argv[4]

    all_league_json = {}

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

    # index_json
    indexjson = indexjson.IndexJson(INDEX_JSON_FOLDER_PATH,
                                    OPENDOTA_INDEX_JSON_FOLDER_PATH)

    # make stat
    league = league.League(leagueid, opendotajson, indexjson)
    league.write_json(league_folder)

    # make all league json
    all_league_json = read_all_league_json(PARENT_LEAGUE_FOLDER_PATH, ALL_LEAGUE_JSON_FILENAME)
    all_league_json[leagueid] = league.get_leaguejson()
    write_all_league_json(PARENT_LEAGUE_FOLDER_PATH, ALL_LEAGUE_JSON_FILENAME, all_league_json)
    print("--end--")
