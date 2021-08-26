# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import Ob
from pyob.exceptions import InvalidObjectError, MixedObjectsError
from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB DUNDER TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObDunderTestCase(PyObFixtureTestCase):
    """ Ob Dunder Test Case """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_add(self):
        """ Ensures that the add dunder method behaves as expected """

        # Get Thailand instance
        tha = self.countries.THA

        # Add None to Thailand
        tha_ = tha + None

        # Assert that adding None to a PyOB object returns an object set of one
        self.assertIsObSet(tha_, count=1)

        # Assert that adding other non-PyOb objects to a PyOb object raises a TypeError
        self.assertRaises(InvalidObjectError, tha.__add__, 50)
        self.assertRaises(InvalidObjectError, tha.__add__, "Japan")
        self.assertRaises(InvalidObjectError, tha.__add__, True)

        # Get Japan instance
        jpn = self.countries.JPN

        # Add Japan to Thailand
        tha_jpn = tha + jpn

        # Assert that adding one PyOb object to another returns a PyOb object set
        self.assertIsObSet(tha_jpn, count=2)

        # Add Japan to Thailand
        tha_jpnkey = tha + "JPN"

        # Assert that adding a key to a PyOb object returns a PyOb object set
        self.assertIsObSet(tha_jpnkey, count=2)

        # Assert that you can add multiple of the same object to an object set
        self.assertIsObSet(tha + jpn + jpn, count=3)
        self.assertIsObSet(tha + "JPN" + "JPN", count=3)

        # Get USA instance
        usa = self.countries.USA

        # Add USA to Japan
        jpn_usa = jpn + usa

        # Assert that you can add an iterable to a PyOb object
        self.assertIsObSet(tha + jpn_usa, count=3)
        self.assertIsObSet(tha + [jpn, usa], count=3)
        self.assertIsObSet(tha + ["JPN", "USA"], count=3)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Ob):
            """ A generic PyOb test class """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(Ob):
            """ A generic PyOb test class """

            # Define keys
            _keys = ("key",)

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ MIXED TYPES
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize A and B instances
        a1 = A()
        b1 = B(key="NoKey")
        b2 = B(key=a1)

        # Initialize assertRaises
        with self.assertRaises(MixedObjectsError):

            # Try to add a B instance to an A instance
            a1 + b1

        # Get b1 and a1 object set
        b1_a1 = b1 + a1

        # Assert that you can add a1 to b1 because a1 is synonymous with b2
        self.assertIsObSet(b1_a1, count=2)

        # Ensure that the resulting object set contains b1 and b2
        self.assertTrue(all(b in b1_a1._obs for b in (b1, b2)))

        # TODO: Add a test to ensure that _keys is an iterable
        # TODO: Make keys backward compatible as synonyms (MAYBE...)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST REPR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_repr(self):
        """ Ensures that the repr dunder method behaves as expected """

        # Get Thailand instance
        tha = self.countries.THA

        # Assert that Thailand representation is correct
        self.assertEqual(repr(tha), "<Country: THA>")

        # Define CountryTest
        class CountryTest(self.Country):
            """ A test class that inherits from Country """

            # Remove string field
            _str = None

        # Replicate Thailand
        tha = CountryTest(**tha.__dict__)

        # Assert that string defaults to the first key, i.e. ISO2
        self.assertEqual(repr(tha), "<Country: TH>")

        # Nullify all keys
        CountryTest._keys = None

        # Assert that the string defaults to the hex of the object
        self.assertEqual(repr(tha), f"<Country: {hex(id(tha))}>")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        # Define A
        class A(Ob):
            """ A test class for instances that will serve as a key """

            # Define string field
            _str = "name"

            # Define init method
            def __init__(self, name):

                # Set name
                self.name = name

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        # Define B
        class B(Ob):
            """ A test class with an A key """

            # Define keys
            _keys = ("key",)

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OB AS KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize A and B instances
        a = A(name="a")
        b = B(key=a)

        # Assert that a PyOb object as a key can be included in __repr__
        self.assertEqual(repr(b), "<B: a>")

        # Nullify A._str
        A._str = None

        # Assert that b's hex is preferred over a's
        # It would just be confusing to give a's hex for the b instance
        self.assertEqual(repr(b), f"<B: {hex(id(b))}>")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST RSHIFT
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_rshift(self):
        """ Ensures that the rshift dunder method behaves as expected """

        # Get Country
        Country = self.Country

        # Get Thailand
        tha = self.countries.THA

        # Assert that rshift works on CountryStore
        self.assertEqual(Country.obs >> "THA", tha)

        # Assert that rshift works on the class as well
        self.assertEqual(Country >> "THA", tha)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr(self):
        """ Ensures that the setattr dunder method behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Ob):
            """ A test class with a key field """

            # Define keys
            _keys = ("key",)

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

        # Initialize key constants
        K1 = "k1"
        K2 = "k2"

        # Initialize A instance
        a = A(key=K1)

        # Assert that k1 is indexed in object store
        self.assertTrue(K1 in A._store._obs_by_key)

        # Assert that k2 is not indexed in object store
        self.assertTrue(K2 not in A._store._obs_by_key)

        # Reassign A instance's key to k2
        a.key = K2

        # Assert that k2 is now indexed in object store
        self.assertTrue(K2 in A._store._obs_by_key)

        # Assert that k2 is no longer indexed in object store
        self.assertTrue(K1 not in A._store._obs_by_key)

        # Assert that you can set the same key without an exception
        # i.e. key check passes if a key exists but already points to current instance
        # Previously the key check was not being smart about this!
        a.key = a.key

        # TODO: Test that keys can be None (not iterable)
        # TODO: Add test to ensure that key indices are not wiped if not is_creating
        # TODO: Test popping of old values (KEY AND UNIQUE)
        # TODO: Test mismatches on exceptions for non-created objects

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST STR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_str(self):
        """ Ensures that the str dunder method behaves as expected """

        # Get Thailand instance
        tha = self.countries.THA

        # Assert that Thailand string is correct
        self.assertEqual(str(tha), "THA")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY TEST
        # └─────────────────────────────────────────────────────────────────────────────

        # Define CountryTest
        class CountryTest(self.Country):
            """ A test class that inherits from Country """

            # Remove string field
            _str = None

        # Replicate Thailand
        tha = CountryTest(**tha.__dict__)

        # Assert that string defaults to the first key, i.e. ISO2
        self.assertEqual(str(tha), "TH")

        # Nullify all keys
        CountryTest._keys = None

        # Assert that the string defaults to the hex of the object
        self.assertEqual(str(tha), hex(id(tha)))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class Child(Ob):
            """ A test class to represent the child of a parent """

            # Define string field
            _str = "parent"

            # Define init method
            def __init__(self, parent):
                """ Init Method """

                # Set parent
                self.parent = parent

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Child):
            """ A class whose string field will point to C """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(Child):
            """ A class whose string field will point to A """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ C
        # └─────────────────────────────────────────────────────────────────────────────

        class C(Child):
            """ A class whose string field will point to B """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILDREN
        # └─────────────────────────────────────────────────────────────────────────────

        # Define parent string
        PARENT = "parent"

        # Initialize child instances
        a = A(PARENT)
        b = B(a)
        c = C(b)

        # Iterate over children
        for child in (a, b, c):

            # Assert that the string is A.parent
            self.assertEqual(str(child), PARENT)

        # Change A.parent to C
        # In an unhandled circumstance, this would lead to infinite recursion
        # i.e. string method would never resolve as: C -> B -> A -> C
        a.parent = c

        # Assert that the string of c is the hex ID of c
        self.assertEqual(str(c), hex(id(c)))


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ SCRIPT
# └─────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Run unittest
    unittest.main()
