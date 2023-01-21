def initial_configs():
    """CONFIGURATION

    Returns:
        initial config variables
    """
    # START HERE

    # Plex
    plex_url = "URL_TO_PLEX_SERVER"
    plex_token = "PLEX_TOKEN"
    PLEX_TV_SHOWS_LIBRARY = "PLEX_TV_SHOW_LIBRARY_TO_MONITOR"
    # PLEX_TV_SHOWS_LIBRARY MUST have access to all shows you wish to watch with this script, if you have more than one librarby normally consider creating a new "ALL SHOWS" library and hiding it from all other users to allow for this, in my experince plex watch history syncs between libraries

    # Sonarr
    sonarr_url = "URL_TO_SONARR_SERVER"
    sonarr_api_key = "SONARR_API_KEY"

    return (plex_url, plex_token, PLEX_TV_SHOWS_LIBRARY, sonarr_url, sonarr_api_key)
