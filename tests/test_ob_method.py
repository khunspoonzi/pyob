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
    # │ TEST LOCALIZED
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_localized(self):
        """ Ensures that the Localized class method behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Assert that Country global store has 250 Country instances
        self.assertIsObStore(self.Country.obs, count=250)

        # Localize Country
        _Country = self.Country.Localized()

        # Assert that Country local store has 0 Country instances
        self.assertIsObStore(_Country.obs, count=0)

        # Assert that localized Country is a different reference
        self.assertNotEqual(id(self.Country), id(_Country))

        # Assert that localized Country store is a different reference
        self.assertNotEqual(id(self.Country._store), id(_Country._store))

        # Get localized Country store
        _store = _Country._store

        # Assert that localized Country object indices are null
        [
            self.assertTrue(not index)
            for index in (_store._obs, _store._obs_by_key, _store._obs_by_unique_field)
        ]

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SET
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_set(self):
        """ Ensures that the Set class method behaves as expected """

        # Initialize new Country object set
        countries = self.Country.Set()

        # Assert that new object set was initialized
        self.assertIsObSet(countries, count=0)

        # Assert that the object class of the object set is Country
        self.assertIs(countries._Ob, self.Country)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
