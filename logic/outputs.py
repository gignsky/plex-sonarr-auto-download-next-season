from datetime import datetime
from settings_constants import print_line


def print_now_analyzing_user_library(user):
    print_line()
    print("Now working on " + user + "'s current series")
    print_line()


def print_current_analyzed_show(show, episode, season):
    """Returns statement to print to tell user what show episode and season caused the final analyzing

    Args:
        show (string): current show
        episode (string): current episode
        season (string): current season

    Returns:
        string: output
    """
    var = (
        "\nAnalyzing TV show '"
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


def print_cannot_match_plex_sonarr_show():
    """Cannot match sonarr show with plex show

    Returns:
        string: output
    """

    var = "Could not match Sonarr show with Plex show. Skipping..."
    print(var)


def print_can_match_plex_sonarr_show(show):
    """Can match sonarr show with plex show

    Returns:
        string: output
    """

    var = (
        "     Matched Plex show with Sonarr show ("
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

    var = "         Assumed season number: " + str(number)
    print(var)


def print_pilot_episode_in_progress(show):
    print(
        f"Current season downloaded is first season in {show} and in-progress episode is pilot. Downloading remaining episodes in this first season."
    )


def print_no_next_season():
    print("     Sonarr indicates that there is no next season. Skipping...")


def print_found_next_season():
    print("     Found a next season on Sonarr. Checking episode availability.")


def print_next_season_has_one_episode():
    print(
        "     Sonarr indicates the next season has at least one episode available. Skipping..."
    )


def print_all_good():
    print("All good! - Monitored and downloaded!")


def print_did_not_meet_threshold():
    print("     Episode did not meet threshold for downloading. Skipping...")


def print_no_in_progress():
    print("No in-progress TV shows found.")


def print_failed_to_access(user):
    print("Failed to access", user, "'s account.")
    print_line()


def print_script_started():
    now = datetime.now()
    print_line()
    print("Script imported all packages and began running core logic at: ")
    print(now)
    print_line()


def print_finished_script():
    now = datetime.now()
    print_line()
    print("Finished at: ")
    print(now)
    print_line()


def print_enter_number():
    print_line()
    print("Please enter the number associated with the account you wish to check")
    print(
        "If you wish to simulate the non-manual script select the option associated with 'ALL'"
    )
    print_line()
