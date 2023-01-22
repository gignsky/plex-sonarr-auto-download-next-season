"""regular outputs in one place so that sonarr and plex interactive outputs are all in one place
"""


def print_met_threshold():
    print("     Met threshold for downloading new episodes.")


def print_can_NOT_find_sonarr_show():
    print(
        "Failed to fetch series from Sonarr. Please double check your Sonarr URL and API Key"
    )


def print_instructing_sonarr():
    print("     Instructing Sonarr to Monitor & Download the next season.")


def print_successful_request():
    print("Request Sent -- SUCCESSFULLY")


def print_failed_request(code):
    print(
        "     FAILED -- to process command. Received status code "
        + str(code.status_code)
    )


def print_test_mode_on():
    print("Test-mode turned ON if it were turned off command be SUCCESSFUL")
