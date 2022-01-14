# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import json

from datetime import datetime
from typing import Optional, Union

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COUNTRY BASE
# └─────────────────────────────────────────────────────────────────────────────────────


class CountryBase:
    """A utility class to represent vanilla country objects"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLASS-LEVEL TYPE HINTS
    # └─────────────────────────────────────────────────────────────────────────────────

    is_un_member_at: Optional[datetime]

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
        """Init Method"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Set country name
        self.name = name
        self.name_native = name_native

        # Set ISO codes
        self.iso2 = iso2
        self.iso3 = iso3

        # Set population
        self.population = population

        # Set latitude and longitude
        self.latitude = latitude
        self.longitude = longitude

        # Set UN member status
        self.is_un_member = is_un_member
        self.is_un_member_at = is_un_member_at

        # Capital 1-to-1


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ COUNTRY
# └─────────────────────────────────────────────────────────────────────────────────────


class Country(CountryBase, PyOb):
    """A utility class to represent PyOb country objects"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB META
    # └─────────────────────────────────────────────────────────────────────────────────

    class PyObMeta:
        """PyOb Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ STORE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define keys
        keys = ("iso2", "iso3")

        # Define unique fields
        unique = ("name", ("latitude", "longitude"))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ APPEARANCE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define display field
        display = "iso3"

        # Define labels
        label_singular = "Country"
        label_plural = "Countries"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE STORE
        # └─────────────────────────────────────────────────────────────────────────────

        def populate_store(Country):
            """Populates the PyOb store"""

            # Open countries fixture
            with open("examples/fixtures/countries.json") as f:

                # Read, initialize, and create Country instances
                [Country(**country) for country in json.load(f)]

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PRE IS UN MEMBER AT
        # └─────────────────────────────────────────────────────────────────────────────

        def pre_is_un_member_at(country, value):
            """Pre-setter for is_un_member_at before setting as an attribute"""

            # Check if value is a string
            if type(value) is str:

                # Split into year, month, day
                year, month, day = [int(v) for v in value.split("-")]

                # Reassign value to datetime object
                value = datetime(year=year, month=month, day=day)

            # Return value
            return value

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POST IS UN MEMBER AT
        # └─────────────────────────────────────────────────────────────────────────────

        def post_is_un_member_at(country, value):
            """Post-setter for is_un_member_at after setting as an attribute"""

            # Determine if is UN member based on whether value is None
            # i.e. If there is a date for when the country became a UN member, we can
            # therefore infer that the country is a UN member
            is_un_member = value is not None

            # Check if is UN member should be updated
            if country.is_un_member != is_un_member:

                # Assign new value to is UN member
                country.is_un_member = is_un_member
