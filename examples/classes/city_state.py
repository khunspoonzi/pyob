# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import json

from datetime import datetime
from typing import Optional, Union

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from examples.classes.city import City
from examples.classes.country import Country


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CITY STATE
# └─────────────────────────────────────────────────────────────────────────────────────


class CityState(City, Country):
    """ A utility class to represent PyOb city state objects """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define keys
    _keys = City._keys + Country._keys

    # Define unique fields
    _unique = City._unique + Country._unique

    # Define labels
    _label_singular = "City State"
    _label_plural = "City States"

    # Define string field
    _str = City._str

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        name: str,
        name_native: str,
        iso2: str,
        iso3: str,
        population: Optional[int],
        latitude: float,
        longitude: float,
        is_un_member: bool,
        is_un_member_at: Union[datetime, str, None],
    ):
        """ Init Method """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PARENT INITIALIZATION
        # └─────────────────────────────────────────────────────────────────────────────

        # Call Country init method
        Country.__init__(
            self,
            name=name,
            name_native=name_native,
            iso2=iso2,
            iso3=iso3,
            population=population,
            latitude=latitude,
            longitude=longitude,
            is_un_member=is_un_member,
            is_un_member_at=is_un_member_at,
        )

        # Call City init method
        City.__init__(
            self,
            country=self,
            name=name,
            population=population,
            latitude=latitude,
            longitude=longitude,
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ _POPULATE STORE
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def _populate_store(cls):
        """ Populates the object store """

        # Open countries fixture
        with open("examples/fixtures/city-states.json") as f:

            # Read, initialize, and create Country instances
            [cls(**cs) for cs in json.load(f)]
