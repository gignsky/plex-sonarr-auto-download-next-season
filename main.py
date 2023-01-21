# v0.5.0

"""
USEAGE
1. Locate #CONFIGURATION
2. Locate #START HERE
3. Input plex and sonarr URL's and API Credentials
4. Configure EPISODE_THRESHOLD with desired integer
5. Make NOTE of "test-mode" option, if you elect to enable test-mode the script will run as normal with the exception of the line that send the download command to sonarr. This should be used when you wish to query your library to see what will be downloaded upon running this script outside of test-mode.

    NOTE Running this script in "test-mode" will additionally disable the scripts ability to set seasons and episodes to "monitored" status

NOTE *** This should work fine if you enter an external URL in the boxes below but services was tested with all devices running on an internal network with hardcoded LAN IP addresses
 """

import sys
from config import initialConfigs
from logic.general_small_logic_functions import user_select
from logic.interactive_functions.plex_interactive import tryPlexUser
from logic.outputs import (
    print_failed_to_access,
    print_finished_script,
    print_now_analyzing_user_library,
)
from settings_constants import settings, test_mode  # import settings
from logic.interactive_functions.sonarr_interactive import fetchSonarrShows
from logic.plex import plex_inital_details
from logic.workhorse import main as workhorse

print_script_started()

# import inital configs
(
    PLEX_URL,
    PLEX_TOKEN,
    PLEX_TV_SHOWS_LIBRARY,
    SONARR_URL,
    SONARR_API_KEY,
) = initialConfigs()  # assign settings

# import general settings
(
    LOG_LEVEL,
    DOWNLOAD_TARGET,
    EPISODE_THRESHOLD,
) = settings()  # assign settings

TEST_MODE = test_mode()

try:
    arg = sys.argv[1]
except IndexError:
    arg = "manual"


def main():
    # fetch all shows that have been added to sonarr
    all_sonarr_shows = fetchSonarrShows(SONARR_URL, SONARR_API_KEY)

    # grab plex account details
    (
        plex_server,
        server_owner_account,
        all_accounts,
        all_accounts_index,
    ) = plex_inital_details(PLEX_URL, PLEX_TOKEN)

    INITAL_PLEX_SERVER = plex_server

    # Check Plex for watched shows that are nearing the end of the season

    # determine if run manually verses in auto-mode
    if arg == "auto":
        x = all_accounts_index  # set start point for while loop
        only_one = False  # ensures script runs for all accounts
    else:
        x = user_select(all_accounts, all_accounts_index)

    if x == all_accounts_index:
        x = 0
        only_one = False  # ensures script runs for all accounts

    else:
        only_one = True  # ensures script runs for selected account

    while x != all_accounts_index:
        # set current account in loop
        current_account_original = all_accounts[x]

        # set current account nice name
        current_account_nice = current_account_original.capitalize()

        # run on first user that is server_owner
        if x == 0:
            print_now_analyzing_user_library(current_account_nice)

            workhorse(
                plex_server,
                all_sonarr_shows,
                EPISODE_THRESHOLD,
                DOWNLOAD_TARGET,
                PLEX_TV_SHOWS_LIBRARY,
                SONARR_URL,
                SONARR_API_KEY,
                TEST_MODE,
            )

        # not first user that is running now
        else:
            print_now_analyzing_user_library(current_account_nice)

            plex_server = tryPlexUser(current_account_original, INITAL_PLEX_SERVER)

            # break upon user failing
            if plex_server != "failed":
                workhorse(
                    plex_server,
                    all_sonarr_shows,
                    EPISODE_THRESHOLD,
                    DOWNLOAD_TARGET,
                    PLEX_TV_SHOWS_LIBRARY,
                    SONARR_URL,
                    SONARR_API_KEY,
                    TEST_MODE,
                )
            else:
                print_failed_to_access(current_account_nice)

        # iterate x up by one
        x = x + 1
        if only_one == True:
            x = all_accounts_index  # resets x to value that ends loop so it only runs on one

    # finish script and print finished time
    print_finished_script()


####
main()
####
