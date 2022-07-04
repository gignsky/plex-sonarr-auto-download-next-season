def initialConfigs():
    """CONFIGURATION

    Returns:
        initial config variables
    """
    # START HERE

    # Plex
    PLEX_URL = "http://IP_TO_PLEX_SERVER:32400/"
    PLEX_TOKEN = "PLEX_TOKEN"
    PLEX_TV_SHOWS_LIBRARY = "TV_SHOW_LIBRARY_NAME_FROM_PLEX"

    # Sonarr
    SONARR_URL = "http://IP_TO_SONARR:8989"
    SONARR_API_KEY = "API_KEY"

    return (
        PLEX_URL,
        PLEX_TOKEN,
        PLEX_TV_SHOWS_LIBRARY,
        SONARR_URL,
        SONARR_API_KEY,
    )
