import requests
from .monitor_functions.monitor_master import main as monitor
from .outputs import *


def fetch_sonarr_shows(SONARR_URL, SONARR_API_KEY):
    """Grabs all shows added to Sonarr

    Args:
        SONARR_URL (string): initally grabbed from config.py
        SONARR_API_KEY (string): initally grabbed from config.py

    Returns:
        sonarr_shows: json
    """

    # grab json string from sonarr api
    sonarr_fetch_shows = requests.get(
        SONARR_URL + "/api/series?apiKey=" + SONARR_API_KEY
    )

    # reset sonarr shows to None
    sonarr_shows = None

    # make sure sonarr connection is successful (i.e. status_code 200, from network codes)
    if sonarr_fetch_shows.status_code == 200:
        sonarr_shows = sonarr_fetch_shows.json()  # convert to json

    # if sonarr connection didn't work it failed hence the below output
    if sonarr_shows is None:

        exit(1)

    return sonarr_shows


def sonarr_download_order(SONARR_URL, SONARR_API_KEY, request_body):
    """Sends a POST request to the Sonarr API to start a download.

    Args:
        SONARR_URL (str): URL for the Sonarr API, initially grabbed from config.py.
        SONARR_API_KEY (str): API key for Sonarr, initially grabbed from config.py.
        request_body (dict): A dictionary containing information about the download request.

    Returns:
        sonarr_command_result: The result of the POST request.
    """
    sonarr_command_result = requests.post(
        SONARR_URL + "/api/command?apiKey=" + SONARR_API_KEY, None, request_body
    )
    return sonarr_command_result


def download_new_episodes(
    sonarr_show,
    sonarr_next_season,
    SONARR_URL,
    SONARR_API_KEY,
    DOWNLOAD_TARGET,
    TEST_MODE,
    assumed_sonarr_season_number_KEY,
):
    """Downloads new episodes of a show from Sonarr.

    Args:
        sonarr_show (dict): A dictionary containing information about the show.
        sonarr_next_season (dict): A dictionary containing information about the next season of the show.
        SONARR_URL (str): URL for the Sonarr API, initially grabbed from config.py.
        SONARR_API_KEY (str): API key for Sonarr, initially grabbed from config.py.
        DOWNLOAD_TARGET (str): Specifies whether to download the full season or individual episodes.
        TEST_MODE (bool): Specifies whether the script is running in test mode.
        assumed_sonarr_season_number_KEY (str):

    Returns:
        status (str): "continue" if request fails, None otherwise.
    """
    print_met_threshold()

    request_body = False
    if DOWNLOAD_TARGET == "FULL_SEASON":

        print_instructing_sonarr()
        request_body = {
            "name": "SeasonSearch",
            "seriesId": sonarr_show["id"],
            "seasonNumber": str(sonarr_next_season["seasonNumber"]),
        }

    if TEST_MODE == False:
        # order sonarr to monitor
        monitor(
            SONARR_URL,
            SONARR_API_KEY,
            request_body["seriesId"],
            request_body["seasonNumber"],
            assumed_sonarr_season_number_KEY,
        )

        # actully order sonarr to download items
        sonarr_command_result = sonarr_download_order(
            SONARR_URL, SONARR_API_KEY, request_body
        )

    elif TEST_MODE == True:
        sonarr_command_result = 99  # 99 is error code to list that test-mode is on note elif command a few lines down

    if sonarr_command_result == 99:
        print_test_mode_on()

    elif sonarr_command_result.status_code == 201:
        # print("test", sonarr_command_result.json()) #XXXX commented out for purposes of cleaning up console readout
        print_successful_request()
        return

    else:
        print_failed_request(sonarr_command_result)
        status = "continue"
        return status
