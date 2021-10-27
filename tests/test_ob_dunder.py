# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import Ob
from pyob.exceptions import (
    DuplicateKeyError,
    InvalidKeyError,
    InvalidObjectError,
    InvalidTypeError,
    UnicityError,
    UnrelatedObjectsError,
)
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

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get countries
        countries = self.Country.obs

        # Get Thailand instance
        tha = countries.THA

        # Add None to Thailand
        tha_ = tha + None

        # Assert that adding None to a PyOB object returns an object set of one
        self.assertIsObSet(tha_, count=1)

        # Assert that adding other non-PyOb objects to a PyOb object raises an error
        [
            self.assertRaises(InvalidObjectError, tha.__add__, val)
            for val in (50, "Japan", True)
        ]

        # Get Japan instance
        jpn = countries.JPN

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
        usa = countries.USA

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
        with self.assertRaises(UnrelatedObjectsError):

            # Try to add a B instance to an A instance
            a1 + b1

        # Get b1 and a1 object set
        b1_a1 = b1 + a1

        # Assert that you can add a1 to b1 because a1 is synonymous with b2
        self.assertEqual(b1_a1, b1 + b2)

        # TODO: Make keys backward compatible as synonyms (MAYBE...)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST REPR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_repr(self):
        """ Ensures that the repr dunder method behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get countries
        countries = self.Country.obs

        # Get Thailand instance
        tha = countries.THA

        # Assert that Thailand representation is correct
        self.assertEqual(repr(tha), "<Country: THA>")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY LOCALIZED
        # └─────────────────────────────────────────────────────────────────────────────

        # Define localized Country
        _Country = self.Country.Localized()

        # Remove string field
        _Country._str = None

        # Replicate Thailand
        tha = _Country(**tha.__dict__)

        # Assert that string defaults to the first key, i.e. ISO2
        self.assertEqual(repr(tha), "<Country: TH>")

        # Nullify all keys
        _Country._keys = None

        # Assert that the string defaults to the hex of the object
        self.assertEqual(repr(tha), f"<Country: {hex(id(tha))}>")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CITY STATE
        # └─────────────────────────────────────────────────────────────────────────────

        # Get city-states
        city_states = self.CityState.obs

        # Get Singapore instance
        sgp = city_states.SGP

        # Assert that Singapore representation is correct
        self.assertEqual(repr(sgp), "<CityState: Singapore>")

        # Assert that you can pass a custom _str argument
        self.assertEqual(sgp.__repr__(_str="iso3"), "<CityState: SGP>")

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
    # │ TEST SETATTR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr(self):
        """ Ensures that the setattr dunder method behaves as expected """

        # Get Thailand
        tha = self.Country.obs.THA

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Try to set invalid type
            tha.iso2 = 35

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR KEYS
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_keys(self):
        """ Ensures that the setattr dunder method behaves as expected """

        # Get Country class
        Country = self.Country

        # Get Thailand
        tha = Country.obs.THA

        # Get United States
        usa = Country.obs.USA

        # Initialize assertRaises block
        with self.assertRaises(InvalidKeyError):

            # Try to set a key to None
            tha.iso2 = None

        # Initialize assertRaises block
        with self.assertRaises(DuplicateKeyError):

            # Try to set a duplicate key
            tha.iso2 = usa.iso2

        # Initialize assertRaises block
        with self.assertRaises(DuplicateKeyError):

            # Try to set a duplicate key of another key field
            tha.iso2 = usa.iso3

        # Get ISO2s
        tha_iso2 = tha.iso2
        usa_iso2 = usa.iso2

        # Get Country store
        _store = Country._store

        # Get objects by key
        _obs_by_key = _store._obs_by_key

        # Define assert baseline helper
        def assertBaseline():

            # Iterate over keys and instances
            for key, instance in ((usa_iso2, usa), (usa_iso2, usa)):

                # Check that keys have been re-indexed
                self.assertTrue(key in _obs_by_key)
                self.assertEqual(_obs_by_key[key], instance)

        # Define assert re-indexed helper
        def assertReIndexed(instance, key_previous, key_current, other, key_other):

            # Check that previous key was removed from index
            self.assertFalse(key_previous in _obs_by_key)

            # Check that current key has been indexed
            self.assertTrue(key_current in _obs_by_key)
            self.assertEqual(_obs_by_key[key_current], instance)

            # Check that other instance remains indexed
            self.assertTrue(key_other in _obs_by_key)
            self.assertEqual(_obs_by_key[key_other], other)

        # Assert that keys are at baseline
        assertBaseline()

        # Define placeholder
        PLACEHOLDER = "placeholder"

        # Set United States ISO2 to new value
        usa.iso2 = PLACEHOLDER

        # Assert that keys have been re-indexed
        assertReIndexed(usa, usa_iso2, PLACEHOLDER, tha, tha_iso2)

        # Ensure that United States ISO2 is now available
        tha.iso2 = usa_iso2

        # Assert that keys have been re-indexed
        assertReIndexed(tha, tha_iso2, usa_iso2, usa, PLACEHOLDER)

        # Reset ISO2 keys
        tha.iso2 = tha_iso2
        usa.iso2 = usa_iso2

        # Assert that keys have returned to baseline
        assertBaseline()

        # Assert that you can set the same key without an exception
        # i.e. key check passes if a key exists but already points to current instance
        # Previously the key check was not being smart about this!
        usa.iso2 = usa.iso2

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR KEYS TRAVERSAL
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_keys_traversal(self):
        """ Ensures that the setattr dunder method behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CONSTANTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define key constants
        KEY = "key"
        KEY_A = "key_a"
        KEY_B = "key_b"
        KEY_C = "key_c"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D, E, F, G
        # │
        # │ Show that keys are checked for all classes with a shared key (inherited)
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Ob):
            """ A PyOb test class """

            # Define keys
            _keys = (KEY,)

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

        class B(A):
            """ A PyOb test class """

        class C(A):
            """ A PyOb test class """

        class D(B):
            """ A PyOb test class """

        class E(B):
            """ A PyOb test class """

        class F(C):
            """ A PyOb test class """

        class G(C):
            """ A PyOb test class """

        # In this case, A is the top-level parent with a defined key

        # Create an instance of A, B, and C
        A(KEY_A), B(KEY_B), C(KEY_C)

        # Iterate over classes
        for Class in (A, B, C, D, E, F, G):

            # Initialize assertRaises block
            with self.assertRaises(DuplicateKeyError):

                # Try to create an instance with a duplicate key
                # This should fail because an A instance already exists with the key
                Class(KEY_A)

            # Iterate over keys
            for key in (KEY_B, KEY_C):

                # Initialize assertRaises block
                with self.assertRaises(DuplicateKeyError):

                    # Try to create an instance with a duplicate key
                    # This should fail regardless of whether the class is a parent,
                    # sibling, or child of B or C because they all share a common key.
                    Class(key)
                    print("--------------------------------------------------------")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D
        # │
        # │ Show that keys are checked going downward and not upward
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Ob):
            """ A PyOb test class """

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

        class B(A):
            """ A PyOb test class """

        class C(A):
            """ A PyOb test class """

            # Define keys
            _keys = (KEY,)

        class D(C):
            """ A PyOb test class """

        # In this case, C is not a top-level parent but does have a defined key

        # Create an instance of A, B, and C
        A(KEY_A), B(KEY_B), C(KEY_C)

        # Iterate over non-key classes
        for Class in (A, B):

            # Ensure that there are no key unicity conflicts
            Class(KEY_A), Class(KEY_B), Class(KEY_C)

            # As A and B are not children of C, we should be able to create instances
            # with a key of KEY_C without a DuplicateKeyError, e.g. the A object set
            # CAN contain two objects where A.key = KEY_C

        # Iterate over key classes
        for Class in (C, D):

            # Initialize assertRaises block
            with self.assertRaises(DuplicateKeyError):

                # Try to create an instance with a duplicate key
                # This should fail because an C instance already exists with the key
                Class(KEY_C)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C
        # │
        # │ Show that keys are specifically NOT checked upward
        # └─────────────────────────────────────────────────────────────────────────────

        # Define key constants
        KEY_1 = "key_1"
        KEY_2 = "key_2"
        KEY_3 = "key_3"

        class A(Ob):
            """ A PyOb test class """

            # Define keys
            _keys = (KEY_1,)

            # Define init method
            def __init__(self, key_1, key_2, key_3):

                # Set keys
                self.key_1 = key_1
                self.key_2 = key_2
                self.key_3 = key_3

        class B(A):
            """ A PyOb test class """

            # Define keys
            _keys = (KEY_2,)

        class C(A):
            """ A PyOb test class """

            # Define keys
            _keys = (KEY_3,)

        # In this case, all classes have the same fields but different keys

        # Create A instances
        A("a1", "b1", "c1")
        B("a2", "a1", "c1")
        C("a3", "b2", "a1")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR PRE AND POST HOOKS
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_pre_and_post_hooks(self):
        """ Ensures that the setattr dunder method behaves as expected """

        # Get Country class
        Country = self.Country

        # Get Thailand
        tha = Country.obs.THA

        # Assert that Thailand is UN member
        self.assertTrue(tha.is_un_member)

        # Get Thailand is UN member status
        is_un_member_at = tha.is_un_member_at

        # Set Thailand is UN member at to None
        tha.is_un_member_at = None

        # Assert that is UN member is now False
        self.assertFalse(tha.is_un_member)

        # Break is UN member at into year, month, and day
        year = is_un_member_at.year
        month = is_un_member_at.month
        day = is_un_member_at.day

        # Set is UN member at as a string, expecting that it will be cleaned
        tha.is_un_member_at = f"{year}-{month}-{day}"

        # Assert that is UN member at was cleaned into its original datetime
        self.assertEqual(tha.is_un_member_at, is_un_member_at)

        # Assert that Thailand is UN member once again
        self.assertTrue(tha.is_un_member)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR UNICITY
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_unicity(self):
        """ Ensures that the setattr dunder method behaves as expected """

        # Get Country class
        Country = self.Country

        # Get Country store
        _store = Country._store

        # Get Thailand
        tha = Country.obs.THA

        # Get United States
        usa = Country.obs.USA

        # Get Thailand and United States name
        tha_name = tha.name
        usa_name = usa.name

        # Get Thailand and United States coordinates
        tha_latitude = tha.latitude
        tha_longitude = tha.longitude
        usa_latitude = usa.latitude
        usa_longitude = usa.longitude

        # Get objects by unique field
        _obs_by_unique_field = _store._obs_by_unique_field

        # Define assert unicity baseline helper
        def assertUnicityBaseline():

            # Iterate over names
            for name in (tha_name, usa_name):

                # Assert that name is indexed as a unique field
                self.assertTrue(name in _obs_by_unique_field["name"])

            # Iterate over coordinates
            for coordinates in (
                (tha_latitude, tha_longitude),
                (usa_latitude, usa_longitude),
            ):

                # Assert that coordinate pairs are indexed together
                self.assertTrue(
                    coordinates in _obs_by_unique_field[("latitude", "longitude")]
                )

        # Define assert unique reindexed
        def assertUniqueReIndexed(
            field, instance, value_previous, value_current, other, value_other
        ):

            # Get field objects
            _field_obs = _obs_by_unique_field[field]

            # Check that previous field value was removed from index
            self.assertFalse(value_previous in _field_obs)

            # Check that current field value has been indexed
            self.assertTrue(value_current in _field_obs)
            self.assertEqual(_field_obs[value_current], instance)

            # Check that other instance remains indexed by field value
            self.assertTrue(value_other in _field_obs)
            self.assertEqual(_field_obs[value_other], other)

        # Assert that unique fields are at baseline
        assertUnicityBaseline()

        # Initialize assertRaises block
        with self.assertRaises(UnicityError):

            # Try to set duplicate a unique field
            tha.name = usa.name

        # Define placeholder
        PLACEHOLDER = "placeholder"

        # Change United States name
        usa.name = PLACEHOLDER

        # Assert that name value has been re-indexed
        assertUniqueReIndexed("name", usa, usa_name, PLACEHOLDER, tha, tha_name)

        # Ensure that United States name is now available
        tha.name = usa_name

        # Assert that name value has been re-indexed
        assertUniqueReIndexed("name", tha, tha_name, usa_name, usa, PLACEHOLDER)

        # Reset name values
        tha.name = tha_name
        usa.name = usa_name

        # Change Thailand latitude to United States latitude
        # tha.latitude = usa.latitude

        # Assert that unique fields have returned to baseline
        assertUnicityBaseline()

        # TODO: Add test to ensure that key indices are not wiped if not is_creating
        # TODO: Test mismatches on exceptions for non-created objects

        # TODO: Test that clean method does not fail on init when pre-referencing

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST STR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_str(self):
        """ Ensures that the str dunder method behaves as expected """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get countries
        countries = self.Country.obs

        # Get Thailand instance
        tha = countries.THA

        # Assert that Thailand string is correct
        self.assertEqual(str(tha), "THA")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY LOCALIZED
        # └─────────────────────────────────────────────────────────────────────────────

        # Define localized Country
        _Country = self.Country.Localized()

        # Remove string field
        _Country._str = None

        # Replicate Thailand
        tha = _Country(**tha.__dict__)

        # Assert that string defaults to the first key, i.e. ISO2
        self.assertEqual(str(tha), "TH")

        # Nullify all keys
        _Country._keys = None

        # Assert that the string defaults to the hex of the object
        self.assertEqual(str(tha), hex(id(tha)))

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CITY-STATE
        # └─────────────────────────────────────────────────────────────────────────────

        # Get city-states
        city_states = self.CityState.obs

        # Get Singapore instance
        sgp = city_states.SGP

        # Assert that Singapore string is correct
        self.assertEqual(str(sgp), "Singapore")

        # Assert that you can pass a custom _str argument
        self.assertEqual(sgp.__str__(_str="iso3"), "SGP")

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
