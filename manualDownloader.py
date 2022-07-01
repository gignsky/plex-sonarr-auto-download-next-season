# gignsky 5.8.22 - PERSONAL - MANUAL - WITH MONITOR FUNCTION
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
import requests
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound
from monitorFunctions.monitorMaster import main as monitor
from config import initialConfigs  # references inital config.py


def main():
    # define printline
    printLine = "============================================="

    # prompt for test-mode
    test_mode = testmode(printLine)

    # import vars from initial configs
    (
        LOG_LEVEL,
        EPISODE_THRESHOLD,
        DOWNLOAD_TARGET,
        PLEX_URL,
        PLEX_TOKEN,
        PLEX_TV_SHOWS_LIBRARY,
        SONARR_URL,
        SONARR_API_KEY,
    ) = initialConfigs()

    # fetch all shows from sonarr
    sonarr_shows = fetchSonarrShows(SONARR_URL, SONARR_API_KEY)

    plex, account = grabPlexDetails(PLEX_URL, PLEX_TOKEN)

    # grab all plex accounts in list
    allAccounts = allAccountsFinder(plex)

    # index position for i when user selects ALL
    allIndex = len(allAccounts)

    # Select User
    x = userSelect(allAccounts, printLine, allIndex)

    if x == allIndex:
        stopper = 0
        x = 0
        z = 0
        if x == 0:
            currentAccountOriginal = allAccounts[x]
            currentAccountNice = currentAccountOriginal.capitalize()
            print(printLine)
            print("Now Working on " + currentAccountNice + "'s Current Series")
            print(printLine)
            workhorse(
                EPISODE_THRESHOLD,
                DOWNLOAD_TARGET,
                PLEX_TV_SHOWS_LIBRARY,
                SONARR_URL,
                SONARR_API_KEY,
                sonarr_shows,
                plex,
                test_mode,
            )
            print(printLine)

        while stopper != 1:
            for x in allAccounts:
                # Check Plex for watched shows that are nearing the end of the season
                currentAccountOriginal = x  # set current account
                # print(currentAccountOriginal)
                currentAccountNice = currentAccountOriginal.capitalize()

                plexAccountWorker(
                    printLine,
                    test_mode,
                    EPISODE_THRESHOLD,
                    DOWNLOAD_TARGET,
                    PLEX_TV_SHOWS_LIBRARY,
                    SONARR_URL,
                    SONARR_API_KEY,
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

        plexAccountWorker(
            printLine,
            test_mode,
            EPISODE_THRESHOLD,
            DOWNLOAD_TARGET,
            PLEX_TV_SHOWS_LIBRARY,
            SONARR_URL,
            SONARR_API_KEY,
            sonarr_shows,
            plex,
            x,
            currentAccountOriginal,
            currentAccountNice,
        )

    now = datetime.now()
    print("Finished at: ")
    print(now)
    print(printLine)


def testmode(printLine):
    """Determine if user wishes to run in test-mode


    Returns:
        Bool with true=yes to test mode
    """
    q = 0
    while q != 1:
        # init prompt
        print(printLine)
        print("Would you like to disable downloads and enable 'test-mode'?")
        print(printLine)

        # actual prompt
        userInput = input("(Y/N)")

        # check user selection
        userInput = userInput.upper()

        if userInput == "Y":
            q = 1
            return bool(1)
        elif userInput == "N":
            q = 1
            return bool(0)
        elif userInput == "YES":
            q = 1
            return bool(1)
        elif userInput == "NO":
            q = 1
            return bool(0)
        else:
            print(printLine)
            print(
                "Appologies, the entered text must be either 'Y', 'N', 'Yes', or 'No'"
            )
            print("Please try again!")
            print(printLine)


def userSelect(allAccounts, printLine, allIndex):
    """Prompt User for Account

    Returns:
        Selected User
    """
    q = 0
    while q != 1:
        i = 0

        # init prompt
        print(printLine)
        print("Please Enter the Number Associated With the Account You Wish to Check")
        print(
            "If you wish to simulate the non-manual script select the option associated with 'ALL'"
        )
        print(printLine)

        # list all users + ALL
        while i != allIndex + 1:
            if i != allIndex:
                item = allAccounts[i]
            elif i == allIndex:
                item = "ALL -- PLEX USER ACCOUNTS"

            print(i, ". ", item)
            i = i + 1

        # request user seletion
        print(printLine)
        userInput = input(
            "Please Enter the Number Associated With the Account You Wish to Check: "
        )

        # check user selection
        try:
            userInput = int(userInput)
            q = 1
        except ValueError:
            print(
                "Entered Value of '",
                userInput,
                "' needs to be an whole number shown on screen",
            )
            q = 0
            print(printLine)
            print("Please Try Again!")
            print(printLine)

    return userInput


def grabPlexDetails(PLEX_URL, PLEX_TOKEN):
    # grab plex details
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    account = plex.myPlexAccount()
    return plex, account


def fetchSonarrShows(SONARR_URL, SONARR_API_KEY):
    sonarr_fetch_shows = requests.get(
        SONARR_URL + "/api/series?apiKey=" + SONARR_API_KEY
    )
    sonarr_shows = None
    if sonarr_fetch_shows.status_code == 200:
        sonarr_shows = sonarr_fetch_shows.json()

    if sonarr_shows == None:
        print(
            "Failed to fetch series from Sonarr. Please double check your Sonarr URL and API Key"
        )
        exit(1)
    return sonarr_shows


def getNames(ALL_PLEX_ACCOUNTS):
    newList = []

    for i in ALL_PLEX_ACCOUNTS:
        item = str(i)
        newItem = item.rsplit(":")[2]  # remove all before second ":"
        newItem2 = newItem.rsplit(">")[0]  # remove ">" after name
        # print(newItem2)
        newList.append(newItem2)

    return newList


def allAccountsFinder(plex):
    # grab all accounts on system
    ALL_PLEX_ACCOUNTS = plex.systemAccounts()

    ALL_PLEX_ACCOUNTS.pop(0)  # remove first output that isn't a user
    allAccounts = getNames(ALL_PLEX_ACCOUNTS)  # converts to just names
    # print(allAccounts)
    # print(allAccounts)
    return allAccounts


def tryPlexUser(currentAccountOriginal, plex):
    try:
        x = plex.switchUser(currentAccountOriginal)
        return x
    except:
        x = "failed"
        return x


def workhorse(
    EPISODE_THRESHOLD,
    DOWNLOAD_TARGET,
    PLEX_TV_SHOWS_LIBRARY,
    SONARR_URL,
    SONARR_API_KEY,
    sonarr_shows,
    plex,
    test_mode,
):
    """Primary Workthread that does the heavy lifting in terms of actually selecting and downloading episodes

    Args:
        from main()
    """
    try:
        plex_tvshows = plex.library.section(PLEX_TV_SHOWS_LIBRARY)
        print("Found Library '" + PLEX_TV_SHOWS_LIBRARY + "'")
    except NotFound:
        print("Library with name '" + PLEX_TV_SHOWS_LIBRARY + "' not found.")
        return Exception("Nothing is currently in progress for this user.")

    PlexTVShowsToCheck = {}

    iterate = plex_tvshows.search(None, None, None, "episode", inProgress=True)

    for episode in iterate:
        plex_show = episode.show()
        # print("plex_show: ", plex_show)
        plex_season = episode.season()
        plex_episode = episode
        plex_show_tvdb = plex_show_tvdb_CHECKER(plex_show)

        # print("plex_show_tvbd: ", plex_show_tvdb)
        # print("plex_show: " + str(plex_show.guids[2].id))

        if not (plex_show_tvdb in PlexTVShowsToCheck):
            PlexTVShowsToCheck[plex_show_tvdb] = {
                "show": plex_show,
                "season": plex_season,
                "episode": plex_episode,
            }
        else:
            if plex_season.index > PlexTVShowsToCheck[plex_show_tvdb]["season"].index:
                # This episode is from a newer season than the existing one. We want the latest, so overwrite
                PlexTVShowsToCheck[plex_show_tvdb] = {
                    "show": plex_show,
                    "season": plex_season,
                    "episode": plex_episode,
                }
            else:
                if (
                    plex_season.index
                    == PlexTVShowsToCheck[plex_show_tvdb]["season"].index
                ):
                    if (
                        plex_episode.index
                        > PlexTVShowsToCheck[plex_show_tvdb]["episode"].index
                    ):
                        # The episode is from the same season and has a higher number. We want the latest, so overwrite
                        PlexTVShowsToCheck[plex_show_tvdb] = {
                            "show": plex_show,
                            "season": plex_season,
                            "episode": plex_episode,
                        }

    if len(PlexTVShowsToCheck) >= 1:
        for tvdbstring in PlexTVShowsToCheck:
            PlexTVShow = PlexTVShowsToCheck[tvdbstring]
            plex_show = PlexTVShow["show"]
            plex_season = PlexTVShow["season"]
            plex_episode = PlexTVShow["episode"]

            print(
                "\nAnalyzing TV Show '"
                + plex_show.title
                + "' with latest in progress episode '"
                + plex_episode.title
                + "' ("
                + plex_season.title
                + ", episode "
                + str(plex_episode.index)
                + ")"
            )
            sonarr_show = False
            for show in sonarr_shows:
                if str(show["tvdbId"]) == plex_show_tvdb_CHECKER(plex_show):
                    sonarr_show = show

            if not sonarr_show:
                print("Could not match Sonarr show with Plex show. SKIPPING...")
                continue

            print(
                "     Matched Plex Show with Sonarr Show ("
                + sonarr_show["title"]
                + " with ID: "
                + str(sonarr_show["id"])
                + ")"
            )
            assumed_sonarr_season_number = plex_season.title
            assumed_sonarr_season_number = int(
                assumed_sonarr_season_number.replace("Season ", "")
            )
            print(
                "         Assumed Sonarr season match: "
                + str(assumed_sonarr_season_number)
            )

            try:
                sonarr_season = sonarr_show["seasons"][
                    int(assumed_sonarr_season_number)
                ]
                print("     Found current season on Sonarr.")
            except IndexError:
                print("     Can't match Sonarr Season. SKIPPING...")
                continue

            if assumed_sonarr_season_number == 1:
                if plex_season.leafCount == 1:
                    print(
                        f"Current Season downloaded is first season in {plex_show} and inprogress episode is pilot. Downloading remaining episodes in this first season."
                    )
                    sonarr_next_season = sonarr_show["seasons"][1]
                    downloadNewEpisodes(
                        sonarr_show,
                        sonarr_next_season,
                        SONARR_URL,
                        SONARR_API_KEY,
                        test_mode,
                        DOWNLOAD_TARGET,
                    )
                else:
                    # print("elsed nothing to report") # was used for testing purposes
                    status = notFirstSeasonChecker(
                        sonarr_show,
                        assumed_sonarr_season_number,
                        plex_episode,
                        EPISODE_THRESHOLD,
                        sonarr_season,
                        SONARR_URL,
                        SONARR_API_KEY,
                        test_mode,
                        DOWNLOAD_TARGET,
                    )
                    if status == "continue":
                        continue
                    else:
                        print("ALL GOOD!")

            else:
                status = notFirstSeasonChecker(
                    sonarr_show,
                    assumed_sonarr_season_number,
                    plex_episode,
                    EPISODE_THRESHOLD,
                    sonarr_season,
                    SONARR_URL,
                    SONARR_API_KEY,
                    test_mode,
                    DOWNLOAD_TARGET,
                )
                if status == "continue":
                    continue
                else:
                    print("ALL GOOD!")

    else:
        print("NO in progress TV shows found.")


def notFirstSeasonChecker(
    sonarr_show,
    assumed_sonarr_season_number,
    plex_episode,
    EPISODE_THRESHOLD,
    sonarr_season,
    SONARR_URL,
    SONARR_API_KEY,
    test_mode,
    DOWNLOAD_TARGET,
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
            SONARR_URL,
            SONARR_API_KEY,
            test_mode,
            DOWNLOAD_TARGET,
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
    SONARR_URL,
    SONARR_API_KEY,
    test_mode,
    DOWNLOAD_TARGET,
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
        sonarr_command_result = sonarrDownloadOrder(
            SONARR_URL, SONARR_API_KEY, requestBody
        )
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


def sonarrDownloadOrder(SONARR_URL, SONARR_API_KEY, requestBody):
    sonarr_command_result = requests.post(
        SONARR_URL + "/api/command?apiKey=" + SONARR_API_KEY, None, requestBody
    )
    return sonarr_command_result


def plex_show_tvdb_CHECKER(plex_show):
    """Prevents end of index issues with some user accounts containing large histories"""
    try:
        x = str(plex_show.guids[2].id).replace("tvdb://", "")
        # print("Index -- No Error")
        return x
    except:
        x = str(plex_show.guids[1].id).replace("tvdb://", "")
        # print("End of Index -- Due to Error")
        return x


def plexAccountWorker(
    printLine,
    test_mode,
    EPISODE_THRESHOLD,
    DOWNLOAD_TARGET,
    PLEX_TV_SHOWS_LIBRARY,
    SONARR_URL,
    SONARR_API_KEY,
    sonarr_shows,
    plex,
    x,
    currentAccountOriginal,
    currentAccountNice,
):
    if x == 0:  # owners account
        currentAccountNice = currentAccountOriginal
        print(printLine)
        print("Now Working on " + currentAccountNice + "'s Current Series")
        print(printLine)
        workhorse(
            EPISODE_THRESHOLD,
            DOWNLOAD_TARGET,
            PLEX_TV_SHOWS_LIBRARY,
            SONARR_URL,
            SONARR_API_KEY,
            sonarr_shows,
            plex,
            test_mode,
        )
        print(printLine)
    else:  # all other accounts
        print(printLine)
        print("Now Working on " + currentAccountNice + "'s Current Series")
        print(printLine)

        plex = tryPlexUser(currentAccountOriginal, plex)  # switch plex user

        # break upon user failing
        if plex != "failed":
            workhorse(
                EPISODE_THRESHOLD,
                DOWNLOAD_TARGET,
                PLEX_TV_SHOWS_LIBRARY,
                SONARR_URL,
                SONARR_API_KEY,
                sonarr_shows,
                plex,
                test_mode,
            )
            print(printLine)
        else:
            print("Failed to Access", currentAccountNice, "'s Account")
            print(printLine)

    return plex


########
main()
########
