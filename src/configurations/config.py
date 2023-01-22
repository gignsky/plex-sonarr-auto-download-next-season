def initialConfigs():
    """CONFIGURATION

    Returns:
        initial config variables
    """
    # START HERE

    # Plex
    PLEX_URL = "URL_TO_PLEX_SERVER"
    PLEX_TOKEN = "PLEX_TOKEN"
    PLEX_TV_SHOWS_LIBRARY = "PLEX_TV_SHOW_LIBRARY_TO_MONITOR"
    # PLEX_TV_SHOWS_LIBRARY MUST have access to all shows you wish to watch with this script, if you have more than one library normally consider creating a new "ALL SHOWS" library and hiding it from all other users to allow for this, in my experience plex watch history syncs between libraries

    # Sonarr
    SONARR_URL = "URL_TO_SONARR_SERVER"
    SONARR_API_KEY = "SONARR_API_KEY"

    return (
        PLEX_URL,
        PLEX_TOKEN,
        PLEX_TV_SHOWS_LIBRARY,
        SONARR_URL,
        SONARR_API_KEY,
    )
