def initialConfigs():
    """CONFIGURATION

    Returns:
        initial config variables
    """
    # General
    LOG_LEVEL = 1
    # Only Full Season at this time. Perhaps 'First Episode' in the future?
    DOWNLOAD_TARGET = "FULL_SEASON"

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

    return (
        LOG_LEVEL,
        EPISODE_THRESHOLD,
        DOWNLOAD_TARGET,
        PLEX_URL,
        PLEX_TOKEN,
        PLEX_TV_SHOWS_LIBRARY,
        SONARR_URL,
        SONARR_API_KEY,
    )
