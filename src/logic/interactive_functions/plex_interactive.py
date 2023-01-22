from plexapi.server import PlexServer


def grabPlexDetails(PLEX_URL, PLEX_TOKEN):
    """grab plex info for server owner

    Args:
        PLEX_URL (string): plex url
        PLEX_TOKEN (string): plex token

    Returns:
        plex_server: plex_server api integration
        server_owner_account: plex server owner account
    """
    # grab plex details
    plex_server = PlexServer(PLEX_URL, PLEX_TOKEN)
    server_owner_account = plex_server.myPlexAccount()
    return plex_server, server_owner_account


def tryPlexUser(currentAccountOriginal, plex):
    """Switch to another plex user

    Args:
        currentAccountOriginal: current account worker is processing
        plex (plex_server - api): api access to server

    Returns:
        _type_: _description_
    """
    try:
        x = plex.switchUser(currentAccountOriginal)
        return x
    except:
        x = "failed"
        return x
