# MANUAL - WITH MONITOR FUNCTION
# manual user selection version of script that allows for scanning plex for in-progress shows and requesting sonarr monitor and download the next season if the next season is not already downloaded or doesn't have any episodes downloaded already.

"""
USEAGE
1. Locate #CONFIGURATION
2. Locate #START HERE
3. Input plex and sonarr URL's and API Credentials
4. Configure EPISODE_THRESHOLD with desired integer
5. Make NOTE of "test-mode" an option that will appear at the beginning of running this script if you select to enable test-mode the script will run as normal with the exception of the line that send the download command to sonarr. This should be used when you wish to query your library to see what will be downloaded upon running this script outside of test-mode.

    NOTE Running this script in "test-mode" will additionally disable the scripts ability to set seasons and episodes to "monitored" status

NOTE *** This should work fine if you enter an external URL in the boxes below but service was tested with all devices running on an internal network with hardcoded LAN IP addresses
 """

from datetime import datetime
from config import *  # import inital config
from userInput import (
    plexUserSelector,
    testmodeQuery,
)  # import testmode query and plex user selector
import accounts as fetch  # import account fetchers
from logic import main as workhorse  # import primary logic flows


def main():

    # prompt for test-mode
    testing = testmodeQuery()

    # fetch all shows from sonarr
    sonarr_shows = fetch.sonarr_shows()

    plex, account = fetch.plex_details()

    # grab all plex accounts in list
    allAccounts = fetch.all_accounts_finder(plex)

    ## THINK ABOUT TRYING THE ZIP Function

    # index position for i when user selects ALL
    allIndex = len(allAccounts)

    # Select User
    x = plexUserSelector(allAccounts, allIndex)

    if x == allIndex:
        stopper = 0
        x = 0
        z = 0
        if x == 0:
            currentAccountOriginal = allAccounts[x]  # set current account
            currentAccountNice = currentAccountOriginal.capitalize()

            print(PRINTLINE)
            print("Now Working on " + currentAccountNice + "'s Current Series")
            print(PRINTLINE)

            workhorse(
                sonarr_shows,
                plex,
                testing,
            )

            print(PRINTLINE)

        while stopper != 1:
            for x in allAccounts:
                # Check Plex for watched shows that are nearing the end of the season
                currentAccountOriginal = x  # set current account
                # print(currentAccountOriginal)
                currentAccountNice = currentAccountOriginal.capitalize()

                fetch.plex_account_iterator(
                    testing,
                    sonarr_shows,
                    plex,
                    x,
                    currentAccountOriginal,
                    currentAccountNice,
                )
                z = z + 1

                # increment until last account
                if z == len(allAccounts):
                    stopper = 1

    else:
        # Check Plex for watched shows that are nearing the end of the season
        currentAccountOriginal = allAccounts[x]  # set current account
        # print(currentAccountOriginal)
        currentAccountNice = currentAccountOriginal.capitalize()

        fetch.plex_account_iterator(
            testing,
            sonarr_shows,
            plex,
            x,
            currentAccountOriginal,
            currentAccountNice,
        )

    now = datetime.now()
    print("Finished at: ")
    print(now)
    print(PRINTLINE)


########
main()
########
