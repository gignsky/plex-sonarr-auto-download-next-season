def initialConfigs():
    """CONFIGURATION

    Returns:
        initial config variables
    """
    # START HERE

    # Plex
    PLEX_URL = "http://192.168.51.4:32400/"
    PLEX_TOKEN = "LnHxpNyxTZf-xbpqJW3D"
    PLEX_TV_SHOWS_LIBRARY = "All Shows"

    # Sonarr
    SONARR_URL = "http://192.168.51.11:8989"
    SONARR_API_KEY = "d1b05072a65a4da0b700bb2fcbee1f56"

    return (
        PLEX_URL,
        PLEX_TOKEN,
        PLEX_TV_SHOWS_LIBRARY,
        SONARR_URL,
        SONARR_API_KEY,
    )
