from plexapi.exceptions import NotFound
from config import *
import sonarrHandler


def main(
    sonarr_shows,
    plex,
    test_mode,
):
    """Primary Workthread that does the heavy lifting in terms of actually selecting and downloading episodes

    Args:
        from main()
    """
    try:
        tvshows = plex.library.section(PLEX_TV_SHOWS_LIBRARY)
        print("Found Library '" + PLEX_TV_SHOWS_LIBRARY + "'")
    except NotFound:
        print("Library with name '" + PLEX_TV_SHOWS_LIBRARY + "' not found.")
        return Exception("Nothing is currently in progress for this user.")

    PlexTVShowsToCheck = {}

    iterate = tvshows.search(None, None, None, "episode", inProgress=True)

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
                    sonarrHandler.downloadNewEpisodes(
                        sonarr_show,
                        sonarr_next_season,
                        test_mode,
                    )
                else:
                    # print("elsed nothing to report") # was used for testing purposes
                    status = sonarrHandler.not_first_season_checker(
                        sonarr_show,
                        assumed_sonarr_season_number,
                        plex_episode,
                        sonarr_season,
                        test_mode,
                    )
                    if status == "continue":
                        continue
                    else:
                        print("ALL GOOD!")

            else:
                status = sonarrHandler.not_first_season_checker(
                    sonarr_show,
                    assumed_sonarr_season_number,
                    plex_episode,
                    sonarr_season,
                    test_mode,
                )
                if status == "continue":
                    continue
                else:
                    print("ALL GOOD!")

    else:
        print("NO in progress TV shows found.")


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
