from .interactive_functions.plex_interactive import grabPlexDetails
from .logical_functions.plex_logical import all_accounts_finder


def plex_inital_details(PLEX_URL, PLEX_TOKEN):
    # grab inital plex details including main owner account and server interaction details
    plex, account = grabPlexDetails(PLEX_URL, PLEX_TOKEN)

    # grab all accounts on plex
    all_accounts = all_accounts_finder(plex)

    # find all accounts length
    all_index = len(all_accounts)

    return (plex, account, all_accounts, all_index)
