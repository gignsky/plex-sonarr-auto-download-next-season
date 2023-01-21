"""regular outputs in one place so that sonarr and plex interactive outputs are all in one place
"""


def print_met_threshold():
    """Prints message indicating threshold met for downloading new episodes"""
    print("Met threshold for downloading new episodes.")


def print_cannot_find_sonarr_show():
    """Prints error message when series not found in Sonarr"""
    print(
        "Failed to fetch series from Sonarr. Please double check your Sonarr URL and API Key."
    )


def print_instructing_sonarr():
    """Prints message indicating instructions sent to Sonarr to monitor and download next season"""
    print("Instructing Sonarr to Monitor & Download the next season.")


def print_successful_request():
    """Prints message indicating a successful request"""
    print("Request Sent -- SUCCESSFULLY")


def print_failed_request(code):
    """Prints message indicating a failed request
    Args:
        code (int): status code of the failed request
    """
    print("FAILED -- to process command. Received status code " + str(code.status_code))


def print_test_mode_on():
    """Prints message indicating test mode is on"""
    print("Test-mode turned ON if it were turned off command be SUCCESSFUL")
