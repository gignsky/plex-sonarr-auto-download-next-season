def print_found_show_in_sonarr():
    """Prints a message indicating that the current season of a show has been found in Sonarr."""
    message = "     Found current season on Sonarr."
    print(message)


def print_did_not_find_show_in_sonarr():
    """Prints a message indicating that the current season of a show cannot be matched in Sonarr."""
    message = "     Can't match Sonarr Season. SKIPPING..."
    print(message)
