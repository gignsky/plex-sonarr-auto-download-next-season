from plexapi.server import PlexServer


def grab_plex_details(PLEX_URL, PLEX_TOKEN):
    """Grabs Plex info for server owner

    Args:
        PLEX_URL (str): Plex server URL
        PLEX_TOKEN (str): Plex server token

    Returns:
        plex_server: Plex server API integration
        server_owner_account: Plex server owner account
    """
    plex_server = PlexServer(PLEX_URL, PLEX_TOKEN)
    server_owner_account = plex_server.myPlexAccount()
    return plex_server, server_owner_account


def try_plex_user(current_account_original, plex):
    """Tries to switch to another Plex user

    Args:
        current_account_original: Current account worker is processing
        plex (plex_server - api): API access to server

    Returns:
        str: "failed" if switching user fails, otherwise the new user's account
    """
    try:
        new_user_account = plex.switchUser(current_account_original)
        return new_user_account
    except:
        return "failed"
