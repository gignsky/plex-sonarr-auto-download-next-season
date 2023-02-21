# sets all episodes in a season to monitored

import json
import requests

# default definitions as this file will be used as a supplemental file; these definitions are only in place to remove the associated error:
base_url = ""
api_key = ""
SONARR_SERIES_ID = -1
season_num = -1
totalSeasonEpisodes = -1


def main(base_url, api_key, season_num, SONARR_SERIES_ID, total_season_episodes):
    """Set all episodes of a season to monitored

    Args:
        base_url (str): url to sonarr
        api_key (str): api for sonarr
        seasonNum (str): sonarr season number of episode
        SONARR_SERIES_ID (str or int): series id of sonarr show, will be converted from str to int if necessary inside this function
        totalSeasonEpisodes (int): total number of episodes in season; this is used to verify that the correct number of episodes is being changed before doing so
    """
    # char vars to ensure they have been set
    check_vars(base_url, api_key, SONARR_SERIES_ID, season_num, total_season_episodes)

    all_episode_path = base_url + "/api/episode?apikey=" + api_key

    # grab all episodes in show
    get_episodes = requests.get(all_episode_path, params={"seriesId": SONARR_SERIES_ID})

    # export body
    data_to_mod = get_episodes.text

    # load data with json object from getEpisodes
    data = json.loads(data_to_mod)

    # loop for getting index's of data's list corresponding to the appropriate season
    episode_IDs = []  # initiate list
    for (
        i
    ) in data:  # loop and add episode id's of episodes in appropriate season to list
        if i["seasonNumber"] == season_num:
            episode_IDs.append(i["id"])

    # sort list
    sorted_IDs = sorted(episode_IDs)

    # check length
    if total_season_episodes != len(episode_IDs):
        "You got a problem homie, there are more episode Id's in this here 'episodeIds' list, why don't you look at this manually"

    modify_episodes(base_url, api_key, sorted_IDs, all_episode_path)


# grab episodes from list & modify to true
def modify_episodes(base_url, api_key, sorted_IDs, send_path):
    """Convert Strings to Json and Back again!"""
    for x in sorted_IDs:
        path = single_episode_path_finder(
            base_url, api_key, x
        )  # grab path for working episode
        single_episode_get = requests.get(path)  # grab single episode detail

        # convert body to python from json
        data_to_mod = single_episode_get.text  # export body
        data = json.loads(
            data_to_mod
        )  # load data with json object from singleEpisodeGet

        # modify to monitored
        data["monitored"] = bool(1)

        # return json object to string
        output = json.dumps(data)

        # send data to sonarr
        requests.put(send_path, output)


def single_episode_path_finder(base_url, api_key, episode_ID):
    """Set Paths"""
    single_episode_path = (
        base_url + "/api/episode/" + str(episode_ID) + "?apikey=" + api_key
    )
    return single_episode_path


def check_vars(base_url, api_key, SONARR_SERIES_ID, season_num, total_season_episodes):
    """ENSURE VARS ARE INPUTTED CORRECTLY
    Nothing Occurs if everything checks out"""
    if (
        base_url == ""
        or api_key == ""
        or SONARR_SERIES_ID == -1
        or season_num == -1
        or total_season_episodes == -1
    ):
        print("Yo Homie! One of the 'monitorEpisodes.py' attributes was NOT set")
        exit
