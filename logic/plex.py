from .interactive_functions.plex_interactive import grab_plex_details
from .logical_functions.plex_logical import all_accounts_finder


def plex_initial_details(plex_url, plex_token):
    # grab initial plex details including main owner account and server interaction details
    plex, account = grab_plex_details(plex_url, plex_token)

    # grab all accounts on plex
    all_accounts = all_accounts_finder(plex)

    # find all accounts length
    all_index = len(all_accounts)

    return (plex, account, all_accounts, all_index)
