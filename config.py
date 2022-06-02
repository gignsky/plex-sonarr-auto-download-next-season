"""CONFIGURATION

Returns:
    initial config variables
"""

# START HERE

# Determines how many episodes before the end of the season a new season should be downloaded.
EPISODE_THRESHOLD = 2

# Plex
PLEX_URL = "http://IP_TO_PLEX_SERVER:32400/"
PLEX_TOKEN = "PLEX_TOKEN"
PLEX_TV_SHOWS_LIBRARY = "TV_SHOW_LIBRARY_NAME_FROM_PLEX"

# Sonarr
SONARR_URL = "http://IP_TO_SONARR:8989"
SONARR_API_KEY = "API_KEY"


# STATIC
# define printline
PRINTLINE = "============================================="

LOG_LEVEL = 1

# Only Full Season at this time. Perhaps 'First Episode' in the future?
DOWNLOAD_TARGET = "FULL_SEASON"
