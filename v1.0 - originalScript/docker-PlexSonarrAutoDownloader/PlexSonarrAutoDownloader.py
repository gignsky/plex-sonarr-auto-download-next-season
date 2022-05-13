import requests
import json
import re
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound

# General
LOG_LEVEL=1
EPISODE_THRESHOLD=2 # Determines how many episodes before the end of the season a new season should be downloaded.
DOWNLOAD_TARGET = "FULL_SEASON" # Only Full Season at this time. Perhaps 'First Episode' in the future?


# Plex
PLEX_URL = "http://someHost:32400/"
PLEX_TOKEN = "TOKEN HERE"
PLEX_TV_SHOWS_LIBRARY = "TV Shows"

# Sonarr
SONARR_URL = "http://someHost:8989"
SONARR_API_KEY = "KEY_HERE"

# Check Plex for watched shows that are nearing the end of the season

sonarr_fetch_shows = requests.get(SONARR_URL + "/api/series?apiKey=" + SONARR_API_KEY)
sonarr_shows = None
if sonarr_fetch_shows.status_code == 200:
    sonarr_shows = sonarr_fetch_shows.json()


if sonarr_shows == None:
    print("Failed to fetch series from Sonarr. Please double check your Sonarr URL and API Key")
    exit(1)


plex = PlexServer(PLEX_URL,PLEX_TOKEN)
account = plex.myPlexAccount()

try:
    tvshows = plex.library.section(PLEX_TV_SHOWS_LIBRARY)
    print("Found Library '" + PLEX_TV_SHOWS_LIBRARY + "'")
except NotFound:
    print("Library with name '" + PLEX_TV_SHOWS_LIBRARY + "' not found.")
    exit(1)

PlexTVShowsToCheck = {}

for episode in tvshows.search(None, None, None, 'episode', inProgress=True):
    plex_show = episode.show()
    plex_season = episode.season()
    plex_episode = episode
    plex_show_tvdb = str(plex_show.guids[2].id).replace("tvdb://","")

    if not (plex_show_tvdb in PlexTVShowsToCheck):
        PlexTVShowsToCheck[plex_show_tvdb] = {'show': plex_show, 'season': plex_season, 'episode': plex_episode}
    else:
        if plex_season.index > PlexTVShowsToCheck[plex_show_tvdb]['season'].index:
            # This episode is from a newer season than the existing one. We want the latest, so overwrite
            PlexTVShowsToCheck[plex_show_tvdb] = {'show': plex_show, 'season': plex_season, 'episode': plex_episode}
        else:
            if plex_season.index == PlexTVShowsToCheck[plex_show_tvdb]['season'].index:
                if plex_episode.index > PlexTVShowsToCheck[plex_show_tvdb]['episode'].index:
                    # The episode is from the same season and has a higher number. We want the latest, so overwrite
                    PlexTVShowsToCheck[plex_show_tvdb] = {'show': plex_show, 'season': plex_season, 'episode': plex_episode}

if len(PlexTVShowsToCheck) >= 1:

    for tvdbstring in PlexTVShowsToCheck:

        PlexTVShow = PlexTVShowsToCheck[tvdbstring]
        plex_show = PlexTVShow['show']
        plex_season = PlexTVShow['season']
        plex_episode = PlexTVShow['episode']

        print("\nAnalyzing TV Show '" + plex_show.title + "' with latest in progress episode '" + plex_episode.title + "' (" + plex_season.title + ", episode " + str(plex_episode.index) + ")")
        sonarr_show = False
        for show in sonarr_shows:
            if str(show['tvdbId']) == str(plex_show.guids[2].id).replace("tvdb://", ""):
                sonarr_show = show

        if not sonarr_show:
            print("Could not match Sonarr show with Plex show. Skipping..")
            continue

        print("     Matched Plex Show with Sonarr Show (" + sonarr_show['title'] + " with ID: " + str(sonarr_show['id']) + ")")
        assumed_sonarr_season_number = plex_season.title
        assumed_sonarr_season_number = int(assumed_sonarr_season_number.replace("Season ", ""))
        #print("Assumed Sonarr season match: " + str(assumed_sonarr_season_number))

        try:
            sonarr_season = sonarr_show['seasons'][int(assumed_sonarr_season_number)]
            print("     Found current season on Sonarr.")
        except IndexError:
            print("     Can't match Sonarr Season. Skipping..")
            continue

        try:
            sonarr_next_season = sonarr_show['seasons'][int(assumed_sonarr_season_number + 1)]
            print("     Found a next season on Sonarr. Checking episode availability.")
        except IndexError:
            print("     Sonarr indicates that there is no next season. Skipping..")
            continue

        if sonarr_next_season['statistics']['episodeCount'] >= 1:
            print("     Sonarr indicates the next season has at least one episode available. Skipping..")
            continue

        episodes_left = abs(sonarr_season['statistics']['totalEpisodeCount'] - episode.index)

        if episodes_left <= EPISODE_THRESHOLD:
            print("     Met threshold for downloading new episodes.")

            requestBody = False
            if DOWNLOAD_TARGET == "FULL_SEASON":
                print("     Instructing Sonarr to download the next season.")
                requestBody = {
                    'name': 'SeasonSearch',
                    'seriesId': sonarr_show['id'],
                    'seasonNumber': str(sonarr_next_season['seasonNumber'])
                }

            sonarr_command_result = requests.post(SONARR_URL + "/api/command?apiKey=" + SONARR_API_KEY, None, requestBody)
            if sonarr_command_result.status_code == 201:
                print(sonarr_command_result.json())
            else:
                print("     Failed to process command. Received status code " + str(sonarr_command_result.status_code))
                continue



        else:
            print("     Episode did not meet threshold for downloading. Skipping..")
            continue
else:
    print("No in progress TV shows found.")







