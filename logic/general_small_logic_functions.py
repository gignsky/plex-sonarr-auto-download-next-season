from logic.outputs import print_enter_number
from settings_constants import printLine


def assumed_season_number_finder(plex_current_season):
    """find assumed season number from plex

    Args:
        plex_current_season (json thingy): the current working season from plex

    Returns:
        int: assumed number of the season that is being worked on
    """

    # assume season number from plex
    assumed_season_number = plex_current_season.title

    # convert to int
    assumed_season_number = int(assumed_season_number.replace("Season ", ""))

    return assumed_season_number


def get_names(ALL_PLEX_ACCOUNTS):
    newList = []

    for i in ALL_PLEX_ACCOUNTS:
        item = str(i)
        newItem = item.rsplit(":")[2]  # remove all before second ":"
        newItem2 = newItem.rsplit(">")[0]  # remove ">" after name
        newList.append(newItem2)

    return newList


def user_select(all_accounts, all_index):
    """Prompt User for Account
    Returns:
        Selected User
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

        # request user selection
        printLine()
        userInput = input(
            "Please Enter the Number Associated With the Account You Wish to Check: "
        )

        # check user selection
        try:
            userInput = int(userInput)
            q = 1
        except ValueError:
            print(
                "Entered Value of '",
                userInput,
                "' needs to be an whole number shown on screen",
            )
            q = 0
            printLine()
            print("Please Try Again!")
            printLine()

    return userInput
