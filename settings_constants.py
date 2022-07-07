def settings():
    """General Settings Configuration

    returns: varibles with general settings most of these will never be used with the exception of test-mode for debugging purposes
    """

    # Currently Unused - Will be used come the logging update, placeholder variable for now
    LOG_LEVEL = 1

    # Only Full Season at this time. Perhaps 'First Episode' in the future?
    DOWNLOAD_TARGET = "FULL_SEASON"

    # Determines how many episodes before the end of the season a new season should be downloaded.
    EPISODE_THRESHOLD = 2

    return (LOG_LEVEL, DOWNLOAD_TARGET, EPISODE_THRESHOLD)


def printLine():
    printLine = "============================================="
    print(printLine)


def test_mode():
    """Make NOTE of "test-mode" an option that will appear at the beginning of running this script if you select to enable test-mode the script will run as normal with the exception of the line that send the download command to sonarr. This should be used when you wish to query your library to see what will be downloaded upon running this script outside of test-mode.
    NOTE Running this script in "test-mode" will additionally disable the scripts ability to set seasons and episodes to "monitored" status
    NOTE TEST_MODE is disabled by default and set to False, to turn on this feature script-wide simply set the below variable to True"""

    TEST_MODE = False

    return TEST_MODE
