# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import Ob
from examples.classes.country import Country


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CITY BASE
# └─────────────────────────────────────────────────────────────────────────────────────


class CityBase:
    """ A utility class to represent vanilla city objects """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INIT METHOD
    # └─────────────────────────────────────────────────────────────────────────────────

    def __init__(self, country: Country, name: str, population: int):
        """ Init Method """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INSTANCE ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Set country
        self.country = country

        # Set country name
        self.name = name

        # Set population
        self.population = population


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CITY
# └─────────────────────────────────────────────────────────────────────────────────────


class City(CityBase, Ob):
    """ A utility class to represent PyOb city objects """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ PYOB ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    # Define keys
    _keys = None

    # Define unique fields
    _unique = (("name", "country"),)

    # Define labels
    _label_singular = "City"
    _label_plural = "Cities"

    # Define string field
    _str = "name"
