# This file helps grab details pertaining to plex and sonarr

from config import *
from plexapi.server import PlexServer
import requests
from logic import main as workhorse  # import primary logic flows

# SONARR
def sonarr_shows():  # grab sonarr details
    sonarr_fetch_shows = requests.get(
        SONARR_URL + "/api/series?apiKey=" + SONARR_API_KEY
    )
    sonarr_shows = None
    if sonarr_fetch_shows.status_code == 200:
        sonarr_shows = sonarr_fetch_shows.json()

    if sonarr_shows == None:
        print(
            "Failed to fetch series from Sonarr. Please double check your Sonarr URL and API Key"
        )
        exit(1)
    return sonarr_shows


# PLEX
def plex_details():  # grab plex details
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    account = plex.myPlexAccount()
    return plex, account


def all_accounts_finder(plex):  # grab all accounts on system
    ALL_PLEX_ACCOUNTS = plex.systemAccounts()

    ALL_PLEX_ACCOUNTS.pop(0)  # remove first output that isn't a user
    allAccounts = getNames(ALL_PLEX_ACCOUNTS)  # converts to just names
    # print(allAccounts)
    # print(allAccounts)
    return allAccounts


def getNames(ALL_PLEX_ACCOUNTS):
    newList = []

    for i in ALL_PLEX_ACCOUNTS:
        item = str(i)
        newItem = item.rsplit(":")[2]  # remove all before second ":"
        newItem2 = newItem.rsplit(">")[0]  # remove ">" after name
        # print(newItem2)
        newList.append(newItem2)

    return newList


def try_plex_user(currentAccountOriginal, plex):
    try:
        x = plex.switchUser(currentAccountOriginal)
        return x
    except:
        x = "failed"
        return x


# Iterate through plex accounts for manual
def plex_account_iterator(
    test_mode,
    sonarr_shows,
    plex,
    x,
    currentAccountOriginal,
    currentAccountNice,
):
    if x == 0:  # owners account
        currentAccountNice = currentAccountOriginal
        print(PRINTLINE)
        print("Now Working on " + currentAccountNice + "'s Current Series")
        print(PRINTLINE)
        workhorse(
            sonarr_shows,
            plex,
            test_mode,
        )
        print(PRINTLINE)
    else:  # all other accounts
        print(PRINTLINE)
        print("Now Working on " + currentAccountNice + "'s Current Series")
        print(PRINTLINE)

        plex = try_plex_user(currentAccountOriginal, plex)  # switch plex user

        # break upon user failing
        if plex != "failed":
            workhorse(
                sonarr_shows,
                plex,
                test_mode,
            )
            print(PRINTLINE)
        else:
            print("Failed to Access", currentAccountNice, "'s Account")
            print(PRINTLINE)

    return plex
