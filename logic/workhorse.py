from .general_small_logic_functions import assumed_season_number_finder
from .logical_functions.outputs import (
    print_did_not_find_show_in_sonarr,
    print_found_show_in_sonarr,
)
from .logical_functions.sonarr_logical import sonarr_key_assigner
from .outputs import (
    print_all_good,
    print_assumed_season_number,
    print_can_not_match_plex_sonarr_show,
    print_can_match_plex_sonarr_show,
    print_current_analyzed_show,
    print_no_in_progress,
)
from .logical_functions.plex_logical import plex_show_tvdb_checker, plex_shows_to_check
from .pilot_episode_worker import main as pilot_worker
from .non_pilot_worker import main as non_pilot_worker
from plexapi.exceptions import NotFound


def main(
    plex_server,
    all_sonarr_shows,
    EPISODE_THRESHOLD,
    DOWNLOAD_TARGET,
    PLEX_TV_SHOWS_LIBRARY,
    SONARR_URL,
    SONARR_API_KEY,
    TEST_MODE,
):

    """Primary Workthread that does the heavy lifting in terms of actually selecting and downloading episodes

    Args:
        from main()
    """

    # try to find plex tv library
    try:
        plex_library = plex_server.library.section(PLEX_TV_SHOWS_LIBRARY)

        print("Found Library '" + PLEX_TV_SHOWS_LIBRARY + "'")

    except NotFound:
        print("Library with name '" + PLEX_TV_SHOWS_LIBRARY + "' not found.")
        return Exception("Nothing is currently in progress for this user.")

    # find in progress shows for current account
    in_progress_shows = plex_library.search(
        None, None, None, "episode", inProgress=True
    )

    plex_tv_shows_to_check = plex_shows_to_check(in_progress_shows)

    # if shows to check is not empty
    if len(plex_tv_shows_to_check) >= 1:
        for tvdb_id_string in plex_tv_shows_to_check:
            plex_current_tv_show = plex_tv_shows_to_check[tvdb_id_string]
            plex_current_show = plex_current_tv_show["show"]
            plex_current_season = plex_current_tv_show["season"]
            plex_current_episode = plex_current_tv_show["episode"]

            # printout current show that is being analyzed
            print_current_analyzed_show(
                plex_current_show, plex_current_episode, plex_current_season
            )

            # set sonarr show to false to keep from repeated trys throwing errors
            sonarr_show = False

            # find sonarr_show from all_sonarr_shows
            for show in all_sonarr_shows:
                if str(show["tvdbId"]) == plex_show_tvdb_CHECKER(plex_current_show):
                    # set sonarr show
                    sonarr_show = show

            # if cant match sonarr show to plex show
            if not sonarr_show:
                print_can_NOT_match_plex_sonarr_show()
                continue

            # if show can be matched unlike above output
            print_can_match_plex_sonarr_show(sonarr_show)

            # assume season number from plex
            assumed_season_number = assumed_season_number_finder(plex_current_season)

            # print assumed season number
            print_assumed_season_number(assumed_season_number)

            # find key for sonarr show
            assumed_sonarr_season_number_KEY = sonarr_key_assigner(
                assumed_season_number, sonarr_show
            )

            # can we find the season in sonarr_show?
            try:
                sonarr_season = sonarr_show["seasons"][assumed_sonarr_season_number_KEY]
                print_found_show_in_sonarr
            except IndexError:
                print_did_NOT_find_show_in_sonarr
                continue

            if assumed_season_number == 1:
                if plex_current_season.leafCount == 1:
                    # pilot episode worker
                    pilot_worker(
                        plex_current_show,
                        sonarr_show,
                        assumed_sonarr_season_number_KEY,
                        SONARR_URL,
                        SONARR_API_KEY,
                        DOWNLOAD_TARGET,
                        EPISODE_THRESHOLD,
                        assumed_season_number,
                        plex_current_episode,
                        sonarr_season,
                        TEST_MODE,
                    )
                else:
                    status = non_pilot_worker(
                        sonarr_show,
                        assumed_season_number,
                        plex_current_episode,
                        EPISODE_THRESHOLD,
                        sonarr_season,
                        SONARR_URL,
                        SONARR_API_KEY,
                        DOWNLOAD_TARGET,
                        TEST_MODE,
                    )
                    if status == "continue":
                        continue
                    else:
                        print("ALL GOOD!")

            else:
                status = non_pilot_worker(
                    sonarr_show,
                    assumed_season_number,
                    plex_current_episode,
                    EPISODE_THRESHOLD,
                    sonarr_season,
                    SONARR_URL,
                    SONARR_API_KEY,
                    DOWNLOAD_TARGET,
                    TEST_MODE,
                )
                if status == "continue":
                    continue
                else:
                    print_all_good()

    # no inprogress tv shows found
    else:
        print_no_in_progress()
