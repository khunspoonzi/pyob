# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import MultipleObjectsError


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ FILTER AND
# └─────────────────────────────────────────────────────────────────────────────────────


def filter_and(_obs, **kwargs):
    """ Filters a series of objects based on a series of keyword arguments (AND) """

    # Return filtered objects
    return [
        _ob
        for _ob in _obs
        if all([getattr(_ob, key) == val for key, val in kwargs.items()])
    ]


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ FILTER BY KEY
# └─────────────────────────────────────────────────────────────────────────────────────


def filter_by_key(_obs, _keys, value, ob_label_plural=None):
    """ Filters a series of objects by a single key value """

    # Initialize keys
    _keys = _keys or []

    # Filter objects by key
    _obs = filter_or(_obs, **{_key: value for _key in _keys})

    # Get distinct object count
    _ob_count = len(set(_obs))

    # Check if object count is greater than 1
    if _ob_count > 1:

        # Lowercase plural label
        ob_label_plural = (ob_label_plural or "Objects").lower()

        # Raise MultipleObjectsError
        raise MultipleObjectsError(
            f"{_ob_count} {ob_label_plural} share a unique key: "
            + ", ".join([str(_ob for _ob in _obs)])
        )

        # NOTE: This should be guarded from happening to begin with but we
        # throw an error here in the event that it does happen

    # Return filtered objects
    return _obs


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ FILTER BY KEYS
# └─────────────────────────────────────────────────────────────────────────────────────


def filter_by_keys(_obs, _keys, values, ob_label_plural=None):
    """ Filters a series of objects by multiple key values """

    # Return filtered objects
    return sum(
        [
            filter_by_key(
                _obs=_obs, _keys=_keys, value=value, ob_label_plural=ob_label_plural
            )
            for value in values
        ],
        [],
    )


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ FILTER OR
# └─────────────────────────────────────────────────────────────────────────────────────


def filter_or(_obs, **kwargs):
    """ Filters a series of objects based on a series of keyword arguments (OR) """

    # Return filtered objects
    return [
        _ob
        for _ob in _obs
        if any([getattr(_ob, key) == val for key, val in kwargs.items()])
    ]
