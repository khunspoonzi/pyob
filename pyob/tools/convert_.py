# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CONVERT OBS DICT TO LIST
# └─────────────────────────────────────────────────────────────────────────────────────


def convert_obs_dict_to_list(_obs):
    """ Converts an object dict to list based on respective counts """

    # Return the sum of object lists by count
    return sum([[k] * v for i, (k, v) in enumerate(_obs.items())], [])
