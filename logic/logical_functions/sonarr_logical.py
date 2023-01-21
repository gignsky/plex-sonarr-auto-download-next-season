def sonarr_key_assigner(season_number, sonarr_show):
    """Finds the associated key for a Sonarr show for a requested season number.

    Args:
        season_number (int): The requested season number.
        sonarr_show (json): All information about a show from Sonarr.

    Returns:
        int: The key associated with the requested season number.
        int: 99 if the loop failed to find the correct value.
    """
    position_var = 0

    for seasons in sonarr_show["seasons"]:
        if seasons["seasonNumber"] == season_number:
            return position_var
        else:
            position_var = position_var + 1

    return 99  # indicates the loop failed without attaining correct value
