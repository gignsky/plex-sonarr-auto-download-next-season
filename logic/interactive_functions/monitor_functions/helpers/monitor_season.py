# Sets season to monitored but not episodes within season

import json
import requests

# Default url and api key for sonarr
base_url = ""
api_key = ""
SONARR_SERIES_ID = -1
season_num = -1


def main(
    base_url, api_key, SONARR_SERIES_ID, season_num, assumed_sonarr_season_number_key
):
    """Set overall season to monitored

    Args:
        base_url (str): The base url of the sonarr instance
        api_key (str): The API key for the sonarr instance
        SONARR_SERIES_ID (int): The series id of the show in sonarr
        season_num (int): The season number of the episodes to be set to monitored
    Returns:
        total_season_episodes (int): The total number of episodes in the given season
    """
    # Verify that the necessary variables have been set
    check_vars(base_url, api_key, SONARR_SERIES_ID, season_num)

    # set paths
    series_path, update_path = path_finder(base_url, api_key, SONARR_SERIES_ID)

    # Get series specific data
    get_series = requests.get(series_path)

    # Get the JSON data for the series
    data_to_mod = get_series.text
    data = json.loads(data_to_mod)

    # Set the monitored flag for the selected season to True
    season_selection = data["seasons"]
    mod_season = season_selection[assumed_sonarr_season_number_key]
    mod_season["monitored"] = True

    # Convert the JSON data back to a string
    output = json.dumps(data)

    # Get the total number of episodes in the selected season
    stats = mod_season["statistics"]
    total_season_episodes = stats["totalEpisodeCount"]

    # Send the modified data to sonarr
    requests.put(update_path, output)

    return total_season_episodes


def path_finder(base_url, api_key, SONARR_SERIES_ID):
    series_spec_path = (
        base_url + "/api/series/" + str(SONARR_SERIES_ID) + "?apikey=" + api_key
    )
    series_update_path = base_url + "/api/series?apikey=" + api_key
    return series_spec_path, series_update_path


def check_vars(base_url, api_key, SONARR_SERIES_ID, season_num):
    """Check that the necessary variables have been set

    Args:
        base_url (str): The base url of the sonarr instance
        api_key (str): The API key for the sonarr instance
        SONARR_SERIES_ID (int): The series id of the show in sonarr
        season_num (int): The season number of the episodes to be set to monitored

    Returns:
        None
    """
    if base_url == "" or api_key == "" or SONARR_SERIES_ID == -1 or season_num == -1:
        print("One of the necessary variables for the script was not set.")
        exit()
