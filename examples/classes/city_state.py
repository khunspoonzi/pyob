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
    """A utility class to represent PyOb city state objects"""

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
    # │ PYOB META
    # └─────────────────────────────────────────────────────────────────────────────────

    class PyObMeta:
        """PyOb Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ APPEARANCE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define display field
        display = City.PyObMeta.display

        # Define labels
        label_singular = "City State"
        label_plural = "City States"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ POPULATE STORE
        # └─────────────────────────────────────────────────────────────────────────────

        def populate_store(CityState):
            """Populates the PyOb store"""

            # Open countries fixture
            with open("examples/fixtures/city-states.json") as f:

                # Read, initialize, and create Country instances
                [CityState(**cs) for cs in json.load(f)]
