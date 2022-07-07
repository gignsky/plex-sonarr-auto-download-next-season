def sonarr_key_assigner(season_number, sonarr_show):
    """find associated key for sonarr show per requested season number

    Args:
        season_number (int): season number value
        sonarr_show (json thingy): all info from sonarr show

    Returns:
        _type_: _description_
    """
    position_var = 0

    for seasons in sonarr_show["seasons"]:
        if seasons["seasonNumber"] == season_number:
            return position_var
        else:
            position_var = position_var + 1

    return 99  # indicates the loop failed without attaining correct value
