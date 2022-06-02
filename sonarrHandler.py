import requests
from config import *
from monitorFunctions.monitorMaster import main as monitor


# Checks
def not_first_season_checker(
    sonarr_show,
    assumed_sonarr_season_number,
    plex_episode,
    sonarr_season,
    test_mode,
):
    # check next season avaliability
    try:
        sonarr_next_season = sonarr_show["seasons"][
            int(assumed_sonarr_season_number + 1)
        ]
        print("     Found a next season on Sonarr. Checking episode availability.")

    except IndexError:
        print("     Sonarr indicates that there is no next season. SKIPPING...")
        status = "continue"
        return status

    # check next season status
    if sonarr_next_season["statistics"]["episodeCount"] >= 1:
        print(
            "     Sonarr indicates the next season has at least one episode available. SKIPPING.."
        )
        status = "continue"
        return status

    episodes_left = abs(
        sonarr_season["statistics"]["totalEpisodeCount"] - plex_episode.index
    )

    if episodes_left <= EPISODE_THRESHOLD:
        status = downloadNewEpisodes(
            sonarr_show,
            sonarr_next_season,
            test_mode,
        )
        if status == "continue":
            status = "continue"
            return status
        else:
            print("ALL GOOD!")

    else:
        print("     Episode did not meet threshold for downloading. SKIPPING..")
        status = "continue"
        return status


# pre-downloader steps
def downloadNewEpisodes(
    sonarr_show,
    sonarr_next_season,
    test_mode,
):

    print("     Met threshold for downloading new episodes.")

    requestBody = False
    if DOWNLOAD_TARGET == "FULL_SEASON":

        print("     Instructing Sonarr to Monitor & Download the next season.")
        requestBody = {
            "name": "SeasonSearch",
            "seriesId": sonarr_show["id"],
            "seasonNumber": str(sonarr_next_season["seasonNumber"]),
        }

    # check test-mode on/off?
    if test_mode == bool(0):
        # order sonarr to monitor
        monitor(
            SONARR_URL,
            SONARR_API_KEY,
            sonarr_show["id"],
            str(sonarr_next_season["seasonNumber"]),
        )

        # actully order sonarr to download items
        sonarr_command_result = sonarrDownloadOrder(requestBody)
    elif test_mode == bool(1):
        sonarr_command_result = 99  # 99 is error code to list that test-mode is on note elif command a few lines down

    # check command status
    if sonarr_command_result == 99:
        print("Test-mode turned on if it were turned off command be SUCCESSFUL")
        return

    elif sonarr_command_result.status_code == 201:
        # print("test", sonarr_command_result.json()) #XXXX commented out for purposes of cleaning up console readout
        print("Request Sent -- SUCCESSFULLY")
        return

    else:
        print(
            "     FAILED -- to process command. Received status code "
            + str(sonarr_command_result.status_code)
        )
        status = "continue"
        return status


# Order Sonarr to Download
def sonarrDownloadOrder(requestBody):
    sonarr_command_result = requests.post(
        SONARR_URL + "/api/command?apiKey=" + SONARR_API_KEY, None, requestBody
    )
    return sonarr_command_result
