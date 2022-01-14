# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PYOB STORE DUNDER TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class PyObStoreDunderTestCase(PyObFixtureTestCase):
    """PyOb Store Dunder Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST GETITEM
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_getitem(self):
        """Ensures that the getitem dunder method behaves as expected"""

        # Get Country
        Country = self.Country

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ INDEX
        # └─────────────────────────────────────────────────────────────────────────────

        # Iterate over index and ISO3 codes
        for i, iso3 in ((0, "AFG"), (246, "ZWE"), (249, "VAT")):

            # Assert that index retrieves the correct country
            self.assertEqual(Country.obs[i], Country.obs >> iso3)

        # Initialize assertRaises block
        with self.assertRaises(IndexError):

            # Try to get a country whose index is out of range
            Country.obs[250]

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ SLICE
        # └─────────────────────────────────────────────────────────────────────────────

        # Define expected country slice
        (istart, iend), iso3s = (1, 5), ["ALA", "ALB", "DZA", "ASM"]

        # Get countries slice
        countries = Country.obs[istart:iend]

        # Assert that the correct countries are sliced
        self.assertEqual([c.iso3 for c in countries], iso3s)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LEN
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_len(self):
        """Ensures that the len dunder method behaves as expected"""

        # Get Country
        Country = self.Country

        # Assert that there are 250 countries
        self.assertAllEqual(len(Country.obs), Country.obs.__len__(), 250)


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()