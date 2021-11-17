# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from typing import Optional

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb
from examples.classes.country import Country


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CITY BASE
# └─────────────────────────────────────────────────────────────────────────────────────


class CityBase:
    """A utility class to represent vanilla city objects"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(
        self,
        country: Country,
        name: str,
        population: Optional[int],
        latitude: float,
        longitude: float,
    ):
        """Init Method"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Set country
        self.country = country

        # Set country name
        self.name = name

        # Set population
        self.population = population

        # Set latitude and longitude
        self.latitude = latitude
        self.longitude = longitude


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CITY
# └─────────────────────────────────────────────────────────────────────────────────────


class City(CityBase, PyOb):
    """A utility class to represent PyOb city objects"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB META
    # └─────────────────────────────────────────────────────────────────────────────────

    class PyObMeta:
        """PyOb Meta Class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ STORE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define keys
        keys = None

        # Define unique fields
        unique = (("name", "country"),)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ APPEARANCE SETTINGS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define display field
        display = "name"

        # Define labels
        label_singular = "City"
        label_plural = "Cities"
