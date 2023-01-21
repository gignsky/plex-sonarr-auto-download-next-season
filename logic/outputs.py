from datetime import datetime
from settings_constants import printLine


def print_now_analyzing_user_library(user):
    printLine()
    print("Now Working on " + user + "'s Current Series")
    printLine()


def print_current_analyzed_show(show, episode, season):
    """returns statement to print to tell user what show episode and season caused the final analyzing

    Args:
        show (string): current show
        episode (string): current episode
        season (string): current season

    Returns:
        string: output
    """
    var = (
        "\nAnalyzing TV Show '"
        + show.title
        + "' with latest in progress episode '"
        + episode.title
        + "' ("
        + season.title
        + ", episode "
        + str(episode.index)
        + ")"
    )

    print(var)


def print_can_NOT_match_plex_sonarr_show():
    """can't match sonarr show with plex show

    Returns:
        string: output
    """

    var = "Could not match Sonarr show with Plex show. SKIPPING..."
    print(var)


def print_can_match_plex_sonarr_show(show):
    """can match sonarr show with plex show

    Returns:
        string: output
    """

    var = (
        "     Matched Plex Show with Sonarr Show ("
        + show["title"]
        + " with ID: "
        + str(show["id"])
        + ")"
    )
    print(var)


def print_assumed_season_number(number):
    """Print the season that script is working with

    Args:
        number (int): assumed season number from workhorse
    """

    var = "         Assumed Season Number: " + str(number)
    print(var)


def print_pilot_episode_in_progress(show):
    print(
        f"Current Season downloaded is first season in {show} and inprogress episode is pilot. Downloading remaining episodes in this first season."
    )


def print_no_next_season():
    print("     Sonarr indicates that there is no next season. SKIPPING...")


def print_found_next_season():
    print("     Found a next season on Sonarr. Checking episode availability.")


def print_next_season_has_one_episode():
    print(
        "     Sonarr indicates the next season has at least one episode available. SKIPPING.."
    )


def print_all_good():
    print("ALL GOOD! - Monitored and Downloaded!")


def print_did_NOT_meet_threshold():
    print("     Episode did not meet threshold for downloading. SKIPPING..")


def print_no_in_progress():
    print("NO in progress TV shows found.")


def print_failed_to_access(user):
    print("Failed to Access", user, "'s Account")
    printLine()


def print_finished_script():
    now = datetime.now()
    printLine()
    print("Finished at: ")
    print(now)
    printLine()


def print_enter_number():
    printLine()
    print("Please Enter the Number Associated With the Account You Wish to Check")
    print(
        "If you wish to simulate the non-manual script select the option associated with 'ALL'"
    )
    printLine()
