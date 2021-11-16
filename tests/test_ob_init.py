# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

from datetime import datetime

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from examples.classes.city import City
from examples.classes.city_state import CityState
from examples.classes.country import Country, CountryBase
from pyob import PyOb
from pyob.exceptions import (
    DuplicateKeyError,
    InvalidKeyError,
    InvalidTypeError,
    UnicityError,
)
from tests.test_cases.pyob import PyObTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GET COUNTRY KWARGS
# └─────────────────────────────────────────────────────────────────────────────────────


def get_country_kwargs(dummy=False):
    """Returns a new dict of common country kwargs"""

    # Check if dummy
    if dummy:

        # Define dummy country kwargs
        country_kwargs = {
            "name": "Dummy",
            "name_native": "Dummy Native",
            "iso2": "DM",
            "iso3": "DMY",
            "population": 10,
            "latitude": 1.1,
            "longitude": 2.2,
            "is_un_member": True,
            "is_un_member_at": datetime(year=1965, month=7, day=14),
        }

    # Otherwise define a normal country
    else:

        # Define common country kwargs
        country_kwargs = {
            "name": "China",
            "name_native": "中国",
            "iso2": "CN",
            "iso3": "CHN",
            "population": 1400000000,
            "latitude": 35.0,
            "longitude": 105.0,
            "is_un_member": True,
            "is_un_member_at": datetime(year=1945, month=10, day=24),
        }

    # Return country kwargs
    return country_kwargs


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB INIT TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObInitTestCase(PyObTestCase):
    """Ob Init Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST CLASS ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_class_attributes(self):
        """Ensures that the test classes have the expected class attributes"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that attributes are correct
        self.assertAttributesCorrect(
            Country,
            ("iso2", "iso3"),
            ("name", ("latitude", "longitude")),
            "Country",
            "Countries",
            "iso3",
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CITY
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that attributes are correct
        self.assertAttributesCorrect(
            City,
            (),
            (("name", "country"),),
            "City",
            "Cities",
            "name",
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CITY-STATE
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that attributes are correct
        self.assertAttributesCorrect(
            CityState,
            ("iso2", "iso3"),
            (("name", "country"), "name", ("latitude", "longitude")),
            "City State",
            "City States",
            "name",
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST INSTANCE ATTRIBUTES
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_instance_attributes(self):
        """Ensures that an object instance attributes are correctly initialized"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY LOCALIZED
        # └─────────────────────────────────────────────────────────────────────────────

        # Define localized Country
        _Country = Country.Localized()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RAW ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Get country kwargs
        country_kwargs = get_country_kwargs()

        # Initialize country instance
        country = _Country(**country_kwargs)

        # Assert that country is an Ob
        self.assertIsOb(country)

        # Iterate over country attributes
        for attr, key in (
            (country.name, "name"),
            (country.name_native, "name_native"),
            (country.iso2, "iso2"),
            (country.iso3, "iso3"),
            (country.population, "population"),
            (country.latitude, "latitude"),
            (country.longitude, "longitude"),
            (country.is_un_member, "is_un_member"),
            (country.is_un_member_at, "is_un_member_at"),
        ):

            # Assert that attribute is correct according to what was passed
            self.assertEqual(attr, country_kwargs[key])

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PRE- AND POST-SETTER ATTRIBUTES
        # └─────────────────────────────────────────────────────────────────────────────

        # Get dummy kwargs
        dummy_kwargs = get_country_kwargs(dummy=True)

        # Stringify is UN member at
        dt = dummy_kwargs["is_un_member_at"]
        string = f"{dt.year}-{dt.month}-{dt.day}"

        # Initialize dummy country
        country_dummy = _Country(
            **{**dummy_kwargs, "is_un_member": False, "is_un_member_at": string}
        )

        # Assert that the string gets converted to a datetime as per _pre method
        self.assertEqual(country_dummy.is_un_member_at, dt)

        # Assert that is UN member is set to True as per _post method
        self.assertEqual(country_dummy.is_un_member, True)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST STORE CONSTRAINTS
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_store_constraints(self):
        """
        Ensures that an object is added to the store upon initialization, and that the
        related constraints behave as expected (key, unicity)
        """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY LOCALIZED
        # └─────────────────────────────────────────────────────────────────────────────

        # Define localized Country
        _Country = Country.Localized()

        # Get country kwargs
        country_kwargs = get_country_kwargs()

        # Initialize country instance
        country = _Country(**country_kwargs)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ ASSERT BASE STATE
        # └─────────────────────────────────────────────────────────────────────────────

        def assertBaseState():
            """A helper to assert a base state after encountering exceptions"""

            # Get store
            _store = _Country._store

            # Assert that CountryTest store has one object
            # i.e. Initialized objects are added to the store
            self.assertIsObStore(_store, count=1)
            self.assertTrue(country in _store._obs)

            # Get objects by key
            _obs_by_key = _store._obs_by_key

            # Assert that CountryTest key index has two keys point to country
            self.assertEqual(len(_obs_by_key), 2)
            self.assertTrue(
                all(
                    [
                        (k in _obs_by_key and _obs_by_key[k] == country)
                        for k in (country.iso2, country.iso3)
                    ]
                )
            )

            # Get objects by unique field
            _obs_by_unique_field = _store._obs_by_unique_field

            # Assert that CountryTest unique fields index has two objecs
            self.assertEqual(len(_obs_by_unique_field), 2)

            # Iterate over unique fields
            for _field, _value in (
                ("name", country.name),
                (("latitude", "longitude"), (country.latitude, country.longitude)),
            ):
                # Assert that field is in objects by unique field
                self.assertTrue(_field in _obs_by_unique_field)

                # Get objects by unique value
                _obs_by_unique_value = _obs_by_unique_field[_field]

                # Assert that value is in objects by unique value
                self.assertTrue(_value in _obs_by_unique_value)

                # Assert that the unique field value points to country
                self.assertEqual(_obs_by_unique_value[_value], country)

        # Assert base state
        assertBaseState()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ DUPLICATE KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get dummy country kwargs
        country_kwargs = get_country_kwargs(dummy=True)

        # Iterate over country ISO codes
        for iso_key, iso_val in (("iso2", country.iso2), ("iso3", country.iso3)):

            # Initialize assertRaises block
            with self.assertRaises(DuplicateKeyError):

                # Try to initialize object with duplicate key
                _Country(**{**country_kwargs, iso_key: iso_val})

            # Assert base state
            assertBaseState()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ UNIQUE CONSTRAINTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Get dummy country kwargs
        country_kwargs = get_country_kwargs(dummy=True)

        # Initialize assertRaises block
        with self.assertRaises(UnicityError):

            # Try to initialize country with same name
            _Country(**{**country_kwargs, "name": country.name})

        # Assert base state
        assertBaseState()

        # Initialize assertRaises block
        with self.assertRaises(UnicityError):

            # Try to initialize country with same latitude and longitude
            _Country(
                **{
                    **country_kwargs,
                    "latitude": country.latitude,
                    "longitude": country.longitude,
                }
            )

        # Assert base state
        assertBaseState()

        # Assert that you can still create a country with the same latitude
        _Country(
            **{
                **country_kwargs,
                "name": "Dummy 1",
                "iso2": "DO",
                "iso3": "DYO",
                "latitude": country.latitude,
            }
        )

        # Assert that you can still create a country with the same longitude
        _Country(
            **{
                **country_kwargs,
                "name": "Dummy 2",
                "iso2": "DT",
                "iso3": "DYT",
                "longitude": country.longitude,
            }
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST TYPE ENFORCEMENT
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_type_enforcement(self):
        """Ensures that types are enforced / disabled upon object initialization"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ TYPED
        # └─────────────────────────────────────────────────────────────────────────────

        # Define CountryTyped
        CountryTyped = Country.Localized()

        # Define invalid key kwargs
        invalid_key_kwargs = get_country_kwargs()
        invalid_key_kwargs["iso2"] = None

        # Initialize assertRaises block
        with self.assertRaises(InvalidKeyError):

            # Try to initialize an instance with a key of None
            CountryTyped(**invalid_key_kwargs)

        # Define invalid type kwargs
        invalid_type_kwargs = get_country_kwargs()
        invalid_type_kwargs["name"] = 5

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Initialize a CountryTest with invalid types
            CountryTyped(**invalid_type_kwargs)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ UNTYPED
        # └─────────────────────────────────────────────────────────────────────────────

        # Define CountryUntyped class
        CountryUntyped = Country.Localized()

        # Set disable type checking to True
        CountryUntyped._disable_type_checking = True

        # Initialize assertRaises block
        with self.assertRaises(InvalidKeyError):

            # Try to initialize an instance with a key of None
            CountryTyped(**invalid_key_kwargs)

        # Initialize untyped country
        country_untyped = CountryUntyped(**invalid_type_kwargs)

        # Assert that untyped country is successfully initialized
        self.assertIsOb(country_untyped)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ TYPE HINT PRECEDENCE
        # └─────────────────────────────────────────────────────────────────────────────

        # NOTE: Do not use Country here as its _pre method will interfere with test

        # Define A class
        class A(PyOb):
            """A test class to to ensure correct type-hint precedence"""

            # Define population type as int
            population: int

            # Define init method
            def __init__(self, population: str):

                # Set population
                self.population = population

        # ASsert that the correct type passes
        self.assertIsOb(A(1000))

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Initialize A instance with incorrect type
            # i.e. Class-level hint takes precedence
            A("1000")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SPEED
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_speed(self):
        """Ensures that an object instance is initialized quick enough"""

        # Get country kwargs
        country_kwargs = get_country_kwargs()

        # Define initialize country base
        def initialize_country_base():
            """Initializes a DummyPyOb instance"""

            # Define localized Country
            Country.Localized()

            # Initialize Pyob Dummy
            CountryBase(**country_kwargs)

        # Define initialize country
        def initialize_country():
            """Initializes a DummyBase instance"""

            # Define localized Country
            _Country = Country.Localized()

            # Initialize dummy base
            _Country(**country_kwargs)

        # NOTE: A new class is defined each time to avoid store conflicts

        # Assert that initialization is no more than x times slower than control
        self.assertTimeLTE(10, initialize_country_base, initialize_country)

        # NOTE: Significant overhead is added to initialization upon defining:
        #   ObMeta.__call__
        #   Ob.__setattr__
        # A lot of overhead is unavoidable by simply declaring custom dunder methods
        # Unfortunately, more attributes the worse since __setattr__ is called each time

        # NOTE: This does not mean that PyOb as a WHOLE is x times slower than normal!


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
