import requests
from .monitor_functions.monitor_master import main as monitor
from .outputs import *


def fetchSonarrShows(SONARR_URL, SONARR_API_KEY):
    """Grabs all shows added to sonarr

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
    if sonarr_shows == None:

        exit(1)

    return sonarr_shows


def sonarrDownloadOrder(SONARR_URL, SONARR_API_KEY, requestBody):
    sonarr_command_result = requests.post(
        SONARR_URL + "/api/command?apiKey=" + SONARR_API_KEY, None, requestBody
    )
    return sonarr_command_result


def downloadNewEpisodes(
    sonarr_show,
    sonarr_next_season,
    SONARR_URL,
    SONARR_API_KEY,
    DOWNLOAD_TARGET,
    TEST_MODE,
):

    print_met_threshold()

    requestBody = False
    if DOWNLOAD_TARGET == "FULL_SEASON":

        print_instructing_sonarr()
        requestBody = {
            "name": "SeasonSearch",
            "seriesId": sonarr_show["id"],
            "seasonNumber": str(sonarr_next_season["seasonNumber"]),
        }

    if TEST_MODE == False:
        # order sonarr to monitor
        monitor(
            SONARR_URL,
            SONARR_API_KEY,
            requestBody["seriesId"],
            requestBody["seasonNumber"],
        )

        # actully order sonarr to download items
        sonarr_command_result = sonarrDownloadOrder(
            SONARR_URL, SONARR_API_KEY, requestBody
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
