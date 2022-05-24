# Sets season to monitored but not episodes within season

import json
import requests

# default definitions as this file will be used as a supplimental file; these defininitions are only in place to remove the associated error:
baseurl = ""
apikey = ""
SONARR_SERIES_ID = -1
seasonNum = -1


def main(baseurl, apikey, SONARR_SERIES_ID, seasonNum):
    """Set overall season to monitored

    Args:
        baseurl (str): url to sonarr
        apikey (str): api for sonarr
        SONARR_SERIES_ID (str or int): series id of sonarr show, will be conerted from str to int if neccecary inside this function
        seasonNum (str): sonarr season number of episode
    Returns:
        totalSeasonEpisodes (_NULL_): total number of episodes in season; this is used to verify that the correct number of episodes is being changed before doing so will be converted to int by monitorEpisodes.py if nececery
    """
    # char vars to ensure they have been set
    checkVars(baseurl, apikey, SONARR_SERIES_ID, seasonNum)

    # set paths
    seriesPath, updatePath = pathfinder(baseurl, apikey, SONARR_SERIES_ID)

    # get series specific data
    getSeries = requests.get(seriesPath)

    # export body
    dataToMod = getSeries.text

    # load data with json object from getSeries.text
    data = json.loads(dataToMod)

    # mods season number to true monitored
    seasonSection = data["seasons"]
    modSeason = seasonSection[int(seasonNum)]
    modSeason["monitored"] = bool(1)

    # return json object back to string
    output = json.dumps(data)

    # find details to set seasons episodes to monitored
    stats = modSeason["statistics"]
    totalSeasonEpisodes = stats["totalEpisodeCount"]

    # send modified body
    requests.put(updatePath, output)

    return totalSeasonEpisodes


def pathfinder(baseurl, apikey, SONARR_SERIES_ID):
    seriesSpecPath = (
        baseurl + "/api/series/" + str(SONARR_SERIES_ID) + "?apikey=" + apikey
    )
    seriesUpdatePath = baseurl + "/api/series?apikey=" + apikey
    return seriesSpecPath, seriesUpdatePath


def checkVars(baseurl, apikey, SONARR_SERIES_ID, seasonNum):

    if baseurl == "" or apikey == "" or SONARR_SERIES_ID == -1 or seasonNum == -1:
        print("+++++++++++++++++++++++++++++++++++++++")
        print("Yo Homie! One of the 'monitorSeason.py' attributes was NOT set")
        print("+++++++++++++++++++++++++++++++++++++++")
        exit
