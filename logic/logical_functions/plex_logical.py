from logic.general_small_logic_functions import get_names


def plex_show_tvdb_checker(plex_show):
    """Checks for the TVDB ID of a show in a Plex library.

    Args:
        plex_show: A show from a Plex library.

    Returns:
        x (str): The TVDB ID of the show, if found.
        None: If the TVDB ID of the show is not found.
    """
    if plex_show.guids != []:
        try:
            x = str(plex_show.guids[2].id).replace("tvdb://", "")
            # print("Index -- No Error")
        except:
            x = str(plex_show.guids[1].id).replace("tvdb://", "")
            # print("End of Index -- Due to Error")
    else:
        x = None

    # TODO NOTE THIS PROBOBLY NEEDS TO BE REFINED INTO ITERATING THROUGH A LOOP SO THAT IF TVDB ID IS NOT IN ONE OF THOSE TWO PLACES IT CAN STILL BE FOUND THIS WILL PRODUCE A PLEX SHOW CANNOT BE FOUND ERROR
    return x


def plex_shows_to_check(in_progress_shows):
    """Finds shows to check in a Plex library.

    Args:
        in_progress_shows (list): A list of shows with the "in-progress" tag.

    Returns:
        list: A list of shows to check, containing information about the show, season, and episode.
    """

    # set tvshows to check to empty
    plex_tv_shows_to_check = {}

    # iterate through inprogress shows
    for episode in in_progress_shows:
        # find overall show
        plex_show = episode.show()
        plex_season = episode.season()
        plex_episode = episode
        plex_show_tvdb_id = plex_show_tvdb_checker(plex_show)

        # check if tvdb is already in tv_shows_to_check
        if not (plex_show_tvdb_id in plex_tv_shows_to_check):
            plex_tv_shows_to_check[plex_show_tvdb_id] = {
                "show": plex_show,
                "season": plex_season,
                "episode": plex_episode,
            }

        # if tvdb_id is not in the to check continue with checks
        else:
            if (
                plex_season.index
                > plex_tv_shows_to_check[plex_show_tvdb_id]["season"].index
            ):
                # This episode is from a newer season than the existing one. We want the latest, so overwrite
                plex_tv_shows_to_check[plex_show_tvdb_id] = {
                    "show": plex_show,
                    "season": plex_season,
                    "episode": plex_episode,
                }
            else:
                if (
                    plex_season.index
                    == plex_tv_shows_to_check[plex_show_tvdb_id]["season"].index
                ):
                    if (
                        plex_episode.index
                        > plex_tv_shows_to_check[plex_show_tvdb_id]["episode"].index
                    ):
                        # The episode is from the same season and has a higher number. We want the latest, so overwrite
                        plex_tv_shows_to_check[plex_show_tvdb_id] = {
                            "show": plex_show,
                            "season": plex_season,
                            "episode": plex_episode,
                        }
    return plex_tv_shows_to_check


def all_accounts_finder(plex):
    """Finds all accounts on a Plex system.

    Args:
        plex (object): A Plex object.

    Returns:
        list: A list of all account names on the Plex system.
    """

    # grab all accounts on system
    all_plex_accounts = plex.systemAccounts()

    all_plex_accounts.pop(0)  # remove first output that isn't a user
    all_accounts = get_names(all_plex_accounts)  # converts to just names

    return all_accounts
