# master controller for monitoring seasons


# from arrapi import SonarrAPI
"""UNCOMMENT ABOVE IMPORT IF YOU TURN ON THE BELOW COMMENTED BLOCK INSIDE MAIN)"""


from .helpers.monitor_season import main as set_season_monitored
from .helpers.monitor_episodes import main as set_episodes_monitored

# config
base_url = ""
api_key = ""
SONARR_SERIES_ID = -1
season_number = -1


def main(base_url, api_key, SONARR_SERIES_ID, season_number,assumed_sonarr_season_number_KEY):

    # char vars to ensure they have been set
    check_vars(base_url, api_key, SONARR_SERIES_ID, season_number)

    """
    # connect with arrapi to sonarr
    sonarr = SonarrAPI(baseurl, apikey)


    # get series from sonar
    series = sonarr.get_series({"series_id": SONARR_SERIES_ID})

    THESE WERE TURNED OFF on PURPOSE###########

    this was turned off in order to protect from accidently downloading unwanted shows
    # ensure series is monitored
    sonarr.edit_series(series, monitored=True)
    """

    # set season to monitored & extract vars for episode monitoring
    total_season_episodes = set_season_monitored(
        base_url, api_key, SONARR_SERIES_ID, season_number,assumed_sonarr_season_number_KEY
    )

    # set episodes inside season to monitored
    set_episodes_monitored(
        base_url, api_key, season_number, SONARR_SERIES_ID, total_season_episodes
    )

    return  # to main thread


def check_vars(base_url, api_key, SONARR_SERIES_ID, season_number):

    if base_url == "" or api_key == "" or SONARR_SERIES_ID == -1 or season_number == -1:
        print("+++++++++++++++++++++++++++++++++++++++")
        print("Yo Homie! One of the 'monitorMaster.py' attributes was NOT set")
        print("+++++++++++++++++++++++++++++++++++++++")
        exit
