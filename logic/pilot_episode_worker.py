from logic.interactive_functions.sonarr_interactive import download_new_episodes
from logic.outputs import print_pilot_episode_in_progress


def main(
    plex_current_show,
    sonarr_show,
    assumed_sonarr_season_number_key,
    SONARR_URL,
    SONARR_API_KEY,
    DOWNLOAD_TARGET,
    EPISODE_THRESHOLD,
    assumed_season_number,
    plex_current_episode,
    sonarr_season,
    test_mode,
):
    print_pilot_episode_in_progress(plex_current_show)

    sonarr_first_season = sonarr_show["seasons"][assumed_sonarr_season_number_key]
    download_new_episodes(
        sonarr_show,
        sonarr_first_season,
        SONARR_URL,
        SONARR_API_KEY,
        DOWNLOAD_TARGET,
        test_mode,
        assumed_sonarr_season_number_key,
    )
