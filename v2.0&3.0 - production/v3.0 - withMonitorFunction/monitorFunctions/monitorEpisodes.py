# sets all episodes in a season to monitored

import json
import requests

# default definitions as this file will be used as a supplimental file; these defininitions are only in place to remove the associated error:
baseurl = ""
apikey = ""
SONARR_SERIES_ID = -1
seasonNum = -1
totalSeasonEpisodes = -1


def main(baseurl, apikey, seasonNum, SONARR_SERIES_ID, totalSeasonEpisodes):
    """Set all episodes of a season to monitored

    Args:
        baseurl (str): url to sonarr
        apikey (str): api for sonarr
        seasonNum (str): sonarr season number of episode
        SONARR_SERIES_ID (str or int): series id of sonarr show, will be conerted from str to int if neccecary inside this function
        totalSeasonEpisodes (int): total number of episodes in season; this is used to verify that the correct number of episodes is being changed before doing so
    """
    # char vars to ensure they have been set
    checkVars(baseurl, apikey, SONARR_SERIES_ID, seasonNum, totalSeasonEpisodes)

    allEpisodePath = baseurl + "/api/episode?apikey=" + apikey

    # grab all episodes in show
    getEpisodes = requests.get(allEpisodePath, params={"seriesId": SONARR_SERIES_ID})

    # export body
    dataToMod = getEpisodes.text

    # load data with json object from getEpisodes
    data = json.loads(dataToMod)

    # loop for getting index's of data's list coresponding to the appropriate season
    episodeIds = []  # initiate list
    for (
        i
    ) in data:  # loop and add episode id's of episodes in appropriate season to list
        if i["seasonNumber"] == seasonNum:
            episodeIds.append(i["id"])

    # sort list
    stortedIds = sorted(episodeIds)

    # check legnth
    if totalSeasonEpisodes != len(episodeIds):
        "You got a problem homie, there are more episode Id's in this here 'episodeIds' list, why don't you look at this manually"

    modifyEpisodes(baseurl, apikey, stortedIds, allEpisodePath)


# grab episodes from list & modify to true
def modifyEpisodes(baseurl, apikey, stortedIds, sendPath):
    """Convert Strings to Json and Back again!"""
    for x in stortedIds:
        path = singleEpisodePathfinder(
            baseurl, apikey, x
        )  # grab path for working episode
        singleEpisodeGet = requests.get(path)  # grab single episode detail

        # convert body to python from json
        dataToMod = singleEpisodeGet.text  # export body
        data = json.loads(dataToMod)  # load data with json object from singleEpisodeGet

        # modify to monitored
        data["monitored"] = bool(1)

        # return json object to string
        output = json.dumps(data)

        # send data to sonarr
        requests.put(sendPath, output)


def singleEpisodePathfinder(baseurl, apikey, epID):
    """Set Paths"""
    singleEpisodePath = baseurl + "/api/episode/" + str(epID) + "?apikey=" + apikey
    return singleEpisodePath


def checkVars(baseurl, apikey, SONARR_SERIES_ID, seasonNum, totalSeasonEpisodes):
    """ENSURE VARS ARE INPUTTED CORRECTLY
    Nothing Occurs if everythings checks out"""
    if (
        baseurl == ""
        or apikey == ""
        or SONARR_SERIES_ID == -1
        or seasonNum == -1
        or totalSeasonEpisodes == -1
    ):
        print("Yo Homie! One of the 'monitorEpisodes.py' attributes was NOT set")
        exit
