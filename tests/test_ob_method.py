# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB METHOD TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObMethodTestCase(PyObFixtureTestCase):
    """ Ob Method Test Case """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SET
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_set(self):
        """ Ensures that the Set class method behaves as expected """

        # Get Country class
        Country = self.Country

        # Initialize new Country object set
        countries = Country.Set()

        # Assert that new object set was initialized
        self.assertIsObSet(countries, count=0)

        # Assert that the object class of the object set is Country
        self.assertIs(countries._Ob, Country)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
