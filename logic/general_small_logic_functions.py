from logic.outputs import print_enter_number
from settings_constants import print_line


def assumed_season_number_finder(plex_current_season):
    """Finds the assumed season number from Plex

    Args:
        plex_current_season (json): The current working season from Plex

    Returns:
        int: The assumed number of the season that is being worked on.
    """

    # assume season number from plex
    assumed_season_number = plex_current_season.title

    # convert to int
    assumed_season_number = int(assumed_season_number.replace("Season ", ""))

    return assumed_season_number


def get_names(ALL_PLEX_ACCOUNTS):
    newList = []

    Args:
        all_plex_accounts (list): A list of account objects.

    Returns:
        list: A list of account names.
    """
    new_list = []

    for account in ALL_PLEX_ACCOUNTS:
        item = str(account)
        new_item = item.rsplit(":")[2]  # remove all before second ":"
        new_item2 = new_item.rsplit(">")[0]  # remove ">" after name
        new_list.append(new_item2)

    return new_list


def user_select(all_accounts, all_index):
    """Prompts the user to select an account.

    Args:
        all_accounts (list): A list of all account names.
        all_index (int): The index of the 'ALL' option in the list of accounts.

    Returns:
        int: The selected user's index in the list of accounts.
    """
    q = 0
    while q != 1:
        i = 0

        # init prompt
        print_enter_number()

        # list all users + ALL
        while i != all_index + 1:
            if i != all_index:
                item = all_accounts[i]
            elif i == all_index:
                item = "ALL -- PLEX USER ACCOUNTS"

            print(i, ". ", item)
            i = i + 1

        # request user seletion
        print_line()
        user_input = input(
            "Please Enter the Number Associated With the Account You Wish to Check: "
        )

        # check user selection
        try:
            user_input = int(user_input)
            q = 1
        except ValueError:
            print(
                "Entered Value of '",
                user_input,
                "' needs to be an whole number shown on screen",
            )
            q = 0
            print_line()
            print("Please Try Again!")
            print_line()

    return user_input
