# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import json
import timeit

from unittest import TestCase

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from examples.classes.country import Country
from pyob import Ob, ObSet, ObStore


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ FIXTURE TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObTestCase(TestCase):
    """ PyOb Test Case """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT ALL EQUAL
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertAllEqual(self, expected_value, *values):
        """ Asserts that all values are equal to an expected value """

        # Iterate over values
        for value in values:

            # Assert that value matches expected value
            self.assertEqual(value, expected_value)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT ATTRIBUTES CORRECT
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertAttributesCorrect(
        self,
        Class,
        _keys,
        _unique,
        _label_singular,
        _label_plural,
        _str,
    ):
        """ Asserts that all class attributes class are correct for testing """

        # Assert that keys are of expected value
        self.assertEqual(Class._keys, _keys)

        # Assert that unique fields are of expected value
        self.assertEqual(Class._unique, _unique)

        # Assert that labels are of expected value
        self.assertEqual(Class._label_singular, _label_singular)
        self.assertEqual(Class._label_plural, _label_plural)

        # Assert that string field is of expected value
        self.assertEqual(Class._str, _str)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT IS OB
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertIsOb(self, item):
        """ Asserts that an item is an Ob instance """

        # Assert that item is an Ob instance
        self.assertIsInstance(item, Ob)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT IS OB SET
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertIsObSet(self, item, count=None, store=False):
        """ Asserts that an item is an instance of ObSet """

        # Assert that item is an instance of ObSet
        self.assertIs(type(item), (ObStore if store else ObSet))

        # Check if count is not None
        if count is not None:

            # Assert that object store count is equal to count
            self.assertEqual(item.count(), count)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT IS OB STORE
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertIsObStore(self, item, count=None):
        """ Asserts that an item is an instance of ObStore """

        # Assert that item is an instance of ObStore
        self.assertIsObSet(item, count=count, store=True)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ASSERT TIME LTE
    # └─────────────────────────────────────────────────────────────────────────────────

    def assertTimeLTE(self, lte, control, *args, number=1000):
        """ Asserts that a time disparity is less than or equal to a percentage """

        # Get control time
        time_control = self.timeit(control, number=number)

        # Iterate over args
        for func in args:

            # Get func time
            time_func = self.timeit(func, number=number)

            # Get disparity
            disparity = time_func / time_control

            # Assert disparity is less than or equal to a percentage
            self.assertLessEqual(disparity, lte)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TIMEIT
    # └─────────────────────────────────────────────────────────────────────────────────

    def timeit(self, func, number=1000):
        """ Times a function or callable for speed tests """

        # Time the function
        return timeit.timeit(func, number=number)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB FIXTURE TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObFixtureTestCase(PyObTestCase):
    """ PyObFixture Test Case """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SET UP CLASS
    # └─────────────────────────────────────────────────────────────────────────────────

    @classmethod
    def setUpClass(cls):
        """ Set Up Class Method """

        # Call parent method
        super().setUpClass()

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRIES
        # └─────────────────────────────────────────────────────────────────────────────

        # Clear Country object store
        Country.obs.clear()

        # Initialize countries
        cls.countries = Country.Set()

        # Open countries fixture
        with open("examples/fixtures/countries.json") as f:

            # Read, initialize, and add countries to object set
            cls.countries += [Country(**country) for country in json.load(f)]

        # Set Country class
        cls.Country = Country
