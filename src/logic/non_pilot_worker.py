from logic.interactive_functions.sonarr_interactive import downloadNewEpisodes
from logic.logical_functions.sonarr_logical import sonarr_key_assigner
from logic.outputs import (
    print_all_good,
    print_did_NOT_meet_threshold,
    print_found_next_season,
    print_next_season_has_one_episode,
    print_no_next_season,
)


def main(
    sonarr_show,
    assumed_season_number,
    plex_episode,
    EPISODE_THRESHOLD,
    sonarr_season,
    SONARR_URL,
    SONARR_API_KEY,
    DOWNLOAD_TARGET,
    TEST_MODE,
):
    assumed_sonarr_season_number_KEY_2 = sonarr_key_assigner(
        assumed_season_number + 1, sonarr_show
    )

    # no next season per direction_finder might make code below unusable
    if assumed_sonarr_season_number_KEY_2 == 99:
        print_no_next_season()
        status = "continue"
        return status

    # check next season availability
    try:
        sonarr_next_season = sonarr_show["seasons"][
            int(assumed_sonarr_season_number_KEY_2)
        ]
        print_found_next_season()

    except IndexError:
        print_no_next_season()  # might be made unnecessary by bit above this try except
        status = "continue"
        return status

    # check next season status
    if sonarr_next_season["statistics"]["episodeCount"] >= 1:
        print_next_season_has_one_episode()
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
            DOWNLOAD_TARGET,
            TEST_MODE,
            assumed_sonarr_season_number_KEY_2
        )
        if status == "continue":
            return status
        else:
            print_all_good()

    else:
        print_did_NOT_meet_threshold()
        status = "continue"
        return status
