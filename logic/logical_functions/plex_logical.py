from logic.general_small_logic_functions import get_names


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


def plex_shows_to_check(inprogress_shows):
    """Find shows to check

    Args:
        inprogress_shows : list of shows with in-progress tag

    Returns:
        list: with shows to check
    """

    # set tvshows to check to empty
    plex_tv_shows_to_check = {}

    # iterate through inprogress shows
    for episode in inprogress_shows:
        # find overall show
        plex_show = episode.show()
        plex_season = episode.season()
        plex_episode = episode
        plex_show_tvdb_ID = plex_show_tvdb_CHECKER(plex_show)

        # check if tvdb is already in tv_shows_to_check
        if not (plex_show_tvdb_ID in plex_tv_shows_to_check):
            plex_tv_shows_to_check[plex_show_tvdb_ID] = {
                "show": plex_show,
                "season": plex_season,
                "episode": plex_episode,
            }

        # if tvdb_ID is not in the to check continue with checks
        else:
            if (
                plex_season.index
                > plex_tv_shows_to_check[plex_show_tvdb_ID]["season"].index
            ):
                # This episode is from a newer season than the existing one. We want the latest, so overwrite
                plex_tv_shows_to_check[plex_show_tvdb_ID] = {
                    "show": plex_show,
                    "season": plex_season,
                    "episode": plex_episode,
                }
            else:
                if (
                    plex_season.index
                    == plex_tv_shows_to_check[plex_show_tvdb_ID]["season"].index
                ):
                    if (
                        plex_episode.index
                        > plex_tv_shows_to_check[plex_show_tvdb_ID]["episode"].index
                    ):
                        # The episode is from the same season and has a higher number. We want the latest, so overwrite
                        plex_tv_shows_to_check[plex_show_tvdb_ID] = {
                            "show": plex_show,
                            "season": plex_season,
                            "episode": plex_episode,
                        }
    return plex_tv_shows_to_check


def all_accounts_finder(plex):
    # grab all accounts on system
    all_plex_accounts = plex.systemAccounts()

    all_plex_accounts.pop(0)  # remove first output that isn't a user
    all_accounts = get_names(all_plex_accounts)  # converts to just names

    return all_accounts
