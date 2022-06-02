from config import *


def testmodeQuery():
    """Determine if user wishes to run in test-mode

    Returns:
        Bool with true=yes to test mode
    """
    q = 0
    while q != 1:
        # init prompt
        print(PRINTLINE)
        print("Would you like to disable downloads and enable 'test-mode'?")
        print(PRINTLINE)

        # actual prompt
        userInput = input("(Y/N)")

        # check user selection
        userInput = userInput.upper()

        if userInput == "Y":
            q = 1
            return bool(1)
        elif userInput == "N":
            q = 1
            return bool(0)
        elif userInput == "YES":
            q = 1
            return bool(1)
        elif userInput == "NO":
            q = 1
            return bool(0)
        else:
            print(PRINTLINE)
            print(
                "Appologies, the entered text must be either 'Y', 'N', 'Yes', or 'No'"
            )
            print("Please try again!")
            print(PRINTLINE)


def plexUserSelector(allAccounts, allIndex):
    """Prompt User for Account

    Returns:
        Selected User
    """
    q = 0
    while q != 1:
        i = 0

        # init prompt
        print(PRINTLINE)
        print("Please Enter the Number Associated With the Account You Wish to Check")
        print(
            "If you wish to simulate the non-manual script select the option associated with 'ALL'"
        )
        print(PRINTLINE)

        # list all users + ALL
        while i != allIndex + 1:
            if i != allIndex:
                item = allAccounts[i]
            elif i == allIndex:
                item = "ALL -- PLEX USER ACCOUNTS"

            print(i, ". ", item)
            i = i + 1

        # request user seletion
        print(PRINTLINE)
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
            print(PRINTLINE)
            print("Please Try Again!")
            print(PRINTLINE)

    return userInput
