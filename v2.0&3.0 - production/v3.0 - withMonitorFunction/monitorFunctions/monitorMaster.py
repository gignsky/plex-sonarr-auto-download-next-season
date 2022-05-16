# master controller for monitoring seasons


# from arrapi import SonarrAPI
"""UNCOMMENT ABOVE IMPORT IF YOU TURN ON THE BELOW COMMENTED BLOCK INSIDE MAIN)"""


from monitorFunctions.monitorSeason import main as setSeasonMonitored
from monitorFunctions.monitorEpisodes import main as setEpisodesMonitored

# config
baseurl = ""
apikey = ""
SONARR_SERIES_ID = -1
seasonNumber = -1


def main(baseurl, apikey, SONARR_SERIES_ID, seasonNumber):

    # char vars to ensure they have been set
    checkVars(baseurl, apikey, SONARR_SERIES_ID, seasonNumber)

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
    totalSeasonEpisodes = setSeasonMonitored(
        baseurl, apikey, SONARR_SERIES_ID, seasonNumber
    )

    # set episodes inside season to monitored
    setEpisodesMonitored(
        baseurl, apikey, seasonNumber, SONARR_SERIES_ID, totalSeasonEpisodes
    )

    return  # to main thread


def checkVars(baseurl, apikey, SONARR_SERIES_ID, seasonNumer):

    if baseurl == "" or apikey == "" or SONARR_SERIES_ID == -1 or seasonNumer == -1:
        print("+++++++++++++++++++++++++++++++++++++++")
        print("Yo Homie! One of the 'monitorMaster.py' attributes was NOT set")
        print("+++++++++++++++++++++++++++++++++++++++")
        exit
