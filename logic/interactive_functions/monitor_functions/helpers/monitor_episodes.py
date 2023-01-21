# sets all episodes in a season to monitored

import json
import requests

# default definitions as this file will be used as a supplimental file; these defininitions are only in place to remove the associated error:
base_url = ""
api_key = ""
SONARR_SERIES_ID = -1
season_num = -1
total_season_episodes = -1


def main(base_url, api_key, season_num, SONARR_SERIES_ID, total_season_episodes):
    """
    Set all episodes of a given season to monitored

    Args:
        base_url (str): The base url of the sonarr instance
        api_key (str): The API key for the sonarr instance
        season_num (int): The season number of the episodes to be set to monitored
        SONARR_SERIES_ID (int): The series id of the show in sonarr
        total_season_episodes (int): The total number of episodes in the given season, used to verify that the correct number of episodes are being changed before doing so
    """
    # Verify that the necessary variables have been set
    check_vars(base_url, api_key, SONARR_SERIES_ID, season_num, total_season_episodes)

    # Construct the url to get all episodes for the series
    all_episode_path = base_url + "/api/episode?apikey=" + api_key

    # Get all episodes for the series
    get_episodes = requests.get(all_episode_path, params={"seriesId": SONARR_SERIES_ID})

    # Get the JSON data for the episodes
    data_to_mod = get_episodes.text
    data = json.loads(data_to_mod)

    # Get the episode ids for the episodes in the given season
    episode_ids = []
    for episode in data:
        if episode["seasonNumber"] == season_num:
            episode_ids.append(episode["id"])

    # Sort the episode ids
    sorted_ids = sorted(episode_ids)

    # Check if the number of episode ids matches the total number of episodes in the season
    if total_season_episodes != len(episode_ids):
        print(
            "The number of episode ids does not match the total number of episodes in the season. Please check manually."
        )

    # Call the function to modify the episodes
    modify_episodes(base_url, api_key, sorted_ids, all_episode_path)


# grab episodes from list & modify to true
def modify_episodes(base_url, api_key, sorted_ids, send_path):
    """Modify episodes to monitored

    Args:
        base_url (str): The base url of the sonarr instance
        api_key (str): The API key for the sonarr instance
        sorted_ids (list): List of episode ids for the episodes to be modified
        send_path (str): The url to send the modified episodes to
    """
    for episode_id in sorted_ids:
        path = single_episode_path_finder(
            base_url, api_key, episode_id
        )  # grab path for working episode
        single_episode_get = requests.get(path)  # grab single episode detail

        # convert body to python from json
        data_to_mod = single_episode_get.text  # export body
        data = json.loads(
            data_to_mod
        )  # load data with json object from singleEpisodeGet

        # modify to monitored
        data["monitored"] = True

        # return json object to string
        output = json.dumps(data)

        # send data to sonarr
        requests.put(send_path, output)


def single_episode_path_finder(base_url, api_key, episode_id):
    """Find the url for a single episode

    Args:
        base_url (str): The base url of the sonarr instance
        api_key (str): The API key for the sonarr instance
        episode_id (int): The id of the episode to get the url for

    Returns:
        str: The url for the given episode
    """
    single_episode_path = (
        base_url + "/api/episode/" + str(episode_id) + "?apikey=" + api_key
    )
    return single_episode_path


def check_vars(base_url, api_key, SONARR_SERIES_ID, season_num, total_season_episodes):
    """Check that the necessary variables have been set

    Args:
        base_url (str): The base url of the sonarr instance
        api_key (str): The API key for the sonarr instance
        SONARR_SERIES_ID (int): The series id of the show in sonarr
        season_num (int): The season number of the episodes to be set to monitored
        total_season_episodes (int): The total number of episodes in the given season

    Returns:
        None
    """
    if (
        base_url == ""
        or api_key == ""
        or SONARR_SERIES_ID == -1
        or season_num == -1
        or total_season_episodes == -1
    ):
        print("One of the necessary variables for the script was not set.")
        exit()
