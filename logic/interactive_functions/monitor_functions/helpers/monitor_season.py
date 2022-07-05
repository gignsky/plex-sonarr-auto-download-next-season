# Sets season to monitored but not episodes within season

import json
import requests

# default definitions as this file will be used as a supplimental file; these defininitions are only in place to remove the associated error:
base_url = ""
api_key = ""
SONARR_SERIES_ID = -1
season_num = -1


def main(base_url, api_key, SONARR_SERIES_ID, season_num):
    """Set overall season to monitored

    Args:
        baseurl (str): url to sonarr
        apikey (str): api for sonarr
        SONARR_SERIES_ID (str or int): series id of sonarr show, will be conerted from str to int if neccecary inside this function
        seasonNum (str): sonarr season number of episode
    Returns:
        totalSeasonEpisodes (_NULL_): total number of episodes in season; this is used to verify that the correct number of episodes is being changed before doing so will be converted to int by monitorEpisodes.py if nececery
    """
    # char vars to ensure they have been set
    check_vars(base_url, api_key, SONARR_SERIES_ID, season_num)

    # set paths
    series_path, update_path = path_finder(base_url, api_key, SONARR_SERIES_ID)

    # get series specific data
    get_series = requests.get(series_path)

    # export body
    data_to_mod = get_series.text

    # load data with json object from getSeries.text
    data = json.loads(data_to_mod)

    # mods season number to true monitored
    season_selection = data["seasons"]
    mod_season = season_selection[int(season_num)]
    mod_season["monitored"] = bool(1)

    # return json object back to string
    output = json.dumps(data)

    # find details to set seasons episodes to monitored
    stats = mod_season["statistics"]
    total_season_episodes = stats["totalEpisodeCount"]

    # send modified body
    requests.put(update_path, output)

    return total_season_episodes


def path_finder(base_url, api_key, SONARR_SERIES_ID):
    series_spec_path = (
        base_url + "/api/series/" + str(SONARR_SERIES_ID) + "?apikey=" + api_key
    )
    series_update_path = base_url + "/api/series?apikey=" + api_key
    return series_spec_path, series_update_path


def check_vars(base_url, api_key, SONARR_SERIES_ID, season_num):

    if base_url == "" or api_key == "" or SONARR_SERIES_ID == -1 or season_num == -1:
        print("+++++++++++++++++++++++++++++++++++++++")
        print("Yo Homie! One of the 'monitorSeason.py' attributes was NOT set")
        print("+++++++++++++++++++++++++++++++++++++++")
        exit
