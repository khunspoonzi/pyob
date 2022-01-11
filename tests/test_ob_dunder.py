# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

from typing import Union

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb
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
    """Ob Dunder Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST ADD
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_add(self):
        """Ensures that the add dunder method behaves as expected"""

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

        class A(PyOb):
            """A generic PyOb test class"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(PyOb):
            """A generic PyOb test class"""

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = ("key",)

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
        """Ensures that the repr dunder method behaves as expected"""

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

        # Nullify display field
        _Country.PyObMeta.display = None

        # Replicate Thailand
        tha = _Country(**tha.__dict__)

        # Assert that string defaults to the first key, i.e. ISO2
        self.assertEqual(repr(tha), "<Country: TH>")

        # Nullify all keys
        _Country.PyObMeta.keys = None

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

        # Assert that you can pass a custom display argument
        self.assertEqual(sgp.__repr__(display="iso3"), "<CityState: SGP>")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        # Define A
        class A(PyOb):
            """A test class for instances that will serve as a key"""

            # Define init method
            def __init__(self, name):

                # Set name
                self.name = name

            # Define PyOb Meta
            class PyObMeta:

                # Define display field
                display = "name"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        # Define B
        class B(PyOb):
            """A test class with an A key"""

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = ("key",)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ OB AS KEY
        # └─────────────────────────────────────────────────────────────────────────────

        # Initialize A and B instances
        a = A(name="a")
        b = B(key=a)

        # Assert that a PyOb object as a key can be included in __repr__
        self.assertEqual(repr(b), "<B: a>")

        # Nullify A.PyObMeta.display
        A.PyObMeta.display = None

        # Assert that b's hex is preferred over a's
        # It would just be confusing to give a's hex for the b instance
        self.assertEqual(repr(b), f"<B: {hex(id(b))}>")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR TYPE CHECKING
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_type_checking(self):
        """Ensures that the setattr dunder method behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get Thailand
        tha = self.Country.obs.THA

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Try to set invalid type
            tha.iso2 = 35

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, number: int):
                """Init Method"""

                # Set number
                self.number = number

        # Create A instance
        a = A(5)

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Try to set a.number to a non-integer
            a.number = 5.5

        # Disable type checking
        A.PyObMeta.disable_type_checking = True

        # Ensure that you can now set a.number to a non-integer
        a.number = 5.5

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR TYPE CHECKING TRAVERSAL
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_type_checking_traversal(self):
        """Ensures that the setattr dunder method behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, number: Union[int, str]):
                """Init Method"""

                # Set number
                self.number = number

        class B(A):
            """A PyOb test class"""

            # Define init method
            def __init__(self, number: str):
                """Init Method"""

                # Call parent init method
                super().__init__(number)

        class C(A):
            """A PyOb test class"""

        # Initialize an instance for each class with an integer
        a, b, c = [Class("5") for Class in (A, B, C)]

        # Iterate over instances
        for instance in (a, b, c):

            # Ensure that number can be set to a string in all cases
            instance.number = "7"

        # Iterate over instances where number can be an integer
        for instance in (a, c):

            # Ensure that number can be set to an integer
            instance.number = 7

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Try to set B instance number to an integer
            b.number = 9

        # Initialize assertRaises block
        with self.assertRaises(InvalidTypeError):

            # Try to set C instance number to a boolean
            c.number = True

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR KEYS
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_keys(self):
        """Ensures that the setattr dunder method behaves as expected"""

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
        _store = Country.PyObMeta.store

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
        """Ensures that the setattr dunder method behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CONSTANTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define key constants
        KEY = "key"
        KEY_A = "key_a"
        KEY_B = "key_b"
        KEY_C = "key_c"
        KEY_D = "key_d"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D, E, F, G
        # │
        # │ Show that keys are checked for all classes with a shared key (inherited)
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY,)

        class B(A):
            """A PyOb test class"""

        class C(A):
            """A PyOb test class"""

        class D(B):
            """A PyOb test class"""

        class E(B):
            """A PyOb test class"""

        class F(C):
            """A PyOb test class"""

        class G(C):
            """A PyOb test class"""

        # In this case, A is the top-level parent with a defined key

        # Create an instance of A, B, and C
        a, b, c = A(KEY_A), B(KEY_B), C(KEY_C)

        # Iterate over classes
        for Class in (A, B, C, D, E, F, G):

            # Initialize assertRaises block
            with self.assertRaises(InvalidKeyError):

                # Try to create an instance where key is None
                Class(None)

            # Iterate over keys
            for key in (KEY_A, KEY_B, KEY_C):

                # Initialize assertRaises block
                with self.assertRaises(DuplicateKeyError):

                    # Try to create an instance with a duplicate key
                    Class(key)

        # Iterate over instances
        for instance, keys in (
            (a, (KEY_B, KEY_C)),
            (b, (KEY_A, KEY_C)),
            (c, (KEY_A, KEY_B)),
        ):

            # Initialize assertRaises block
            with self.assertRaises(InvalidKeyError):

                # Try to set key to None
                instance.key = None

            # Iterate over keys
            for key in keys:

                # Initialize assertRaises block
                with self.assertRaises(DuplicateKeyError):

                    # Try to set key of existing instance to existing key
                    instance.key = key

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D
        # │
        # │ Show that keys are checked going downward according to inheritance
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, key):

                # Set key
                self.key = key

        class B(A):
            """A PyOb test class"""

        class C(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY,)

        class D(C):
            """A PyOb test class"""

        # In this case, C is not a top-level parent but does have a defined key

        # Create an instance of A and B
        A(KEY_A), B(KEY_B)

        # Create an instance of C and D
        c, d = C(KEY_C), D(KEY_D)

        # Iterate over non-key classes
        for Class in (A, B):

            # Ensure that you can set key to None (as Class.key isn't actually a key)
            Class(None)

            # Ensure that there are no key unicity conflicts
            Class(KEY_A), Class(KEY_B), Class(KEY_C), Class(KEY_D)

            # As A and B are not children of C, we should be able to create instances
            # with a key of KEY_C and KEY_D without a DuplicateKeyError,
            # e.g. the A object set CAN contain two objects where A.key = KEY_C / KEY_D

        # Iterate over key classes
        for Class in (C, D):

            # Initialize assertRaises block
            with self.assertRaises(InvalidKeyError):

                # Try to create an instance where key is None
                Class(None)

            # Iterate over args
            for arg in (KEY_C, KEY_D):

                # Initialize assertRaises block
                with self.assertRaises(DuplicateKeyError):

                    # Try to create an instance with a duplicate key
                    # This should fail because an C instance already exists with the key
                    Class(arg)

        # Iterate over key instances
        for instance, key in ((c, KEY_D), (d, KEY_C)):

            # Initialize assertRaises block
            with self.assertRaises(InvalidKeyError):

                # Try to set key to None
                instance.key = None

            # Initialize assertRaises block
            with self.assertRaises(DuplicateKeyError):

                # Try to set instance key to an existing key
                instance.key = key

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C
        # │
        # │ Show that keys are specifically NOT checked upward if not inherited
        # └─────────────────────────────────────────────────────────────────────────────

        # Define key constants
        KEY_1 = "key_1"
        KEY_2 = "key_2"
        KEY_3 = "key_3"

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, key_1, key_2, key_3):

                # Set keys
                self.key_1 = key_1
                self.key_2 = key_2
                self.key_3 = key_3

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_1,)

        class B(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_2,)

        class C(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define keys
                keys = (KEY_3,)

        # In this case, all classes have the same fields but different key definitions

        # Define unique constant
        UNIQUE = "unique"

        # Define assertDuplicateKey helper
        def assertDuplicateKey(Class, *args):

            # Initialize assertRaises block
            with self.assertRaises(DuplicateKeyError):

                # Try to initialize instance
                Class(*args)

        # Create A instance
        A("a1", "b1", "c1")

        # Assert that key 1 is enforced
        assertDuplicateKey(A, "a1", UNIQUE, UNIQUE)

        # Create B instance where b.key_2 == a.key_1
        # There should be no conflict since key_2 is not a key for A
        B("a2", "a1", "c1")

        # Assert that key 1 is still enforced on B
        assertDuplicateKey(B, "a1", UNIQUE, UNIQUE)

        # Assert that key 2 is enforced on B
        assertDuplicateKey(B, UNIQUE, "a1", UNIQUE)

        # Create C instance where c.key_2 == b.key_2 and c.key_3 == a.key_1
        # There should be no conflict since key_2 is not a key for C and
        # key_3 is not a key for A
        C("a3", "a1", "a1")

        # Create C instance where c.key_2 == b.key_2 and c.key_3 == b.key_3
        # There should be no conflict since key_2 is not a key for C and
        # key_3 is not a key for B
        C("a4", "a1", "c1")

        # Assert that key 1 is still enforced on C
        assertDuplicateKey(C, "a1", UNIQUE, UNIQUE)

        # Assert that key 3 is enforced on C
        assertDuplicateKey(C, UNIQUE, UNIQUE, "a1")

        # Assert that key 3 is enforced on C
        assertDuplicateKey(C, UNIQUE, UNIQUE, "c1")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR PRE AND POST HOOKS
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_pre_and_post_hooks(self):
        """Ensures that the setattr dunder method behaves as expected"""

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
        """Ensures that the setattr dunder method behaves as expected"""

        # Get Country class
        Country = self.Country

        # Get Country store
        _store = Country.PyObMeta.store

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
        tha.latitude = usa_latitude

        # Assert that latitude + longitude has been re-indexed
        assertUniqueReIndexed(
            ("latitude", "longitude"),
            tha,
            (tha_latitude, tha_longitude),
            (usa_latitude, tha_longitude),
            usa,
            (usa_latitude, usa_longitude),
        )

        # Initialize assertRaises block
        with self.assertRaises(UnicityError):

            # Try to change Thailand longitude to United States longitude
            tha.longitude = usa.longitude

        # Restore Thailand latitude
        tha.latitude = tha_latitude

        # Change Thailand longitude to United States longitude
        tha.longitude = usa.longitude

        # Initialize assertRaises block
        with self.assertRaises(UnicityError):

            # Try to change Thailand latitude to United States latitude
            tha.latitude = usa.latitude

        # Restore Thailand longitude
        tha.longitude = tha_longitude

        # Assert that unique fields have returned to baseline
        assertUnicityBaseline()

        # TODO: Add test to ensure that key indices are not wiped if not is_creating
        # TODO: Test mismatches on exceptions for non-created objects
        # TODO: Test that clean method does not fail on init when pre-referencing

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SETATTR UNICITY TRAVERSAL
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_setattr_unicity_traversal(self):
        """Ensures that the setattr dunder method behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CONSTANTS
        # └─────────────────────────────────────────────────────────────────────────────

        # Define unique constants
        UNIQUE = "unique"
        UNIQUE_1 = "unique_1"
        UNIQUE_2 = "unique_2"
        UNIQUE_3 = "unique_3"

        UNIQUE_A = "unique_a"
        UNIQUE_B = "unique_b"
        UNIQUE_C = "unique_c"
        UNIQUE_D = "unique_d"
        UNIQUE_E = "unique_e"
        UNIQUE_F = "unique_f"
        UNIQUE_G = "unique_g"
        UNIQUE_H = "unique_h"
        UNIQUE_I = "unique_i"
        UNIQUE_J = "unique_j"
        UNIQUE_K = "unique_k"
        UNIQUE_L = "unique_l"

        UNIQUE_A_GROUP = (UNIQUE_A, UNIQUE_B, UNIQUE_C)
        UNIQUE_B_GROUP = (UNIQUE_D, UNIQUE_E, UNIQUE_F)
        UNIQUE_C_GROUP = (UNIQUE_G, UNIQUE_H, UNIQUE_I)
        UNIQUE_D_GROUP = (UNIQUE_J, UNIQUE_K, UNIQUE_L)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ PERMUTATE
        # └─────────────────────────────────────────────────────────────────────────────

        # Define permutate helper
        def permutate(u1, u2, u3):
            """Returns a list of permutations of three unique fields"""

            # Return permutations
            return [
                (u1, u2, u3),
                (UNIQUE, u2, u3),
                (u1, UNIQUE, u3),
                (u1, u2, UNIQUE),
                (u1, UNIQUE, UNIQUE),
            ]

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D, E, F, G
        # │
        # │ Show that unique fields are checked for all inherited classes
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, unique_1, unique_2, unique_3):

                # Set unique fields
                self.unique_1 = unique_1
                self.unique_2 = unique_2
                self.unique_3 = unique_3

            # Define PyOb Meta
            class PyObMeta:

                # Define unique fields
                unique = (UNIQUE_1, (UNIQUE_2, UNIQUE_3))

        class B(A):
            """A PyOb test class"""

        class C(A):
            """A PyOb test class"""

        class D(B):
            """A PyOb test class"""

        class E(B):
            """A PyOb test class"""

        class F(C):
            """A PyOb test class"""

        class G(C):
            """A PyOb test class"""

        # In this case, A is the top-level parent with defined unique fields

        # Create an instance of A, B, and C
        a, b, c = (A(*UNIQUE_A_GROUP), B(*UNIQUE_B_GROUP), C(*UNIQUE_C_GROUP))

        # Iterate over classes
        for Class in (A, B, C, D, E, F, G):

            # Iterate over args
            for args in (
                # A Instance
                *permutate(*UNIQUE_A_GROUP),
                # B Instance
                *permutate(*UNIQUE_B_GROUP),
                # C Instance
                *permutate(*UNIQUE_C_GROUP),
            ):

                # Initialize assertRaises block
                with self.assertRaises(UnicityError):

                    # Try to create an instance with a duplicate key
                    Class(*args)

        # Define set unique field helper
        def set_unique_fields(*instances):

            # Iterate over instances
            for instance, singles, togethers in instances:

                # Iterate over singles
                for single in singles:

                    # Initialize assertRaises block
                    with self.assertRaises(UnicityError):

                        # Try to set existing unique value
                        instance.unique_1 = single

                # Iterate over togethers
                for unique_2, unique_3 in togethers:

                    # Get original values
                    unique_2_original = instance.unique_2
                    unique_3_original = instance.unique_3

                    # Set unique 2 value
                    instance.unique_2 = unique_2

                    # Initialize assertRaises block
                    with self.assertRaises(UnicityError):

                        # Try to set unique 3 value
                        instance.unique_3 = unique_3

                    # Reset original values
                    instance.unique_2 = unique_2_original
                    instance.unique_3 = unique_3_original

        # Test setting unique fields
        set_unique_fields(
            (a, (UNIQUE_D, UNIQUE_G), [(UNIQUE_E, UNIQUE_F), (UNIQUE_H, UNIQUE_I)]),
            (b, (UNIQUE_A, UNIQUE_G), [(UNIQUE_B, UNIQUE_C), (UNIQUE_H, UNIQUE_I)]),
            (c, (UNIQUE_A, UNIQUE_D), [(UNIQUE_B, UNIQUE_C), (UNIQUE_E, UNIQUE_F)]),
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C, D
        # │
        # │ Show that unique fields are checked going downward according to inheritance
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(self, unique_1, unique_2, unique_3):

                # Set unique fields
                self.unique_1 = unique_1
                self.unique_2 = unique_2
                self.unique_3 = unique_3

        class B(A):
            """A PyOb test class"""

        class C(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define unique fields
                unique = (UNIQUE_1, (UNIQUE_2, UNIQUE_3))

        class D(C):
            """A PyOb test class"""

        # In this case, C is not a top-level parent but has defined unique fields

        # Create an instance of A and B
        A(*UNIQUE_A_GROUP), B(*UNIQUE_B_GROUP)

        # Create an instance of C and D
        c, d = C(*UNIQUE_C_GROUP), D(*UNIQUE_D_GROUP)

        # Iterate over non-key classes
        for Class in (A, B):

            # Ensure that there are no field unicity conflicts
            Class(*UNIQUE_A_GROUP)
            Class(*UNIQUE_B_GROUP)
            Class(*UNIQUE_C_GROUP)
            Class(*UNIQUE_D_GROUP)

            # As A and B are not children of C, we should be able to create instances
            # with reused fields without a UnicityError,

        # Iterate over key classes
        for Class in (C, D):

            # Iterate over args
            for args in (
                *permutate(*UNIQUE_C_GROUP),
                *permutate(*UNIQUE_D_GROUP),
            ):

                # Initialize assertRaises block
                with self.assertRaises(UnicityError):

                    # Try to create an instance with a duplicate field
                    # This should fail because an instance already exists with the field
                    Class(*args)

        # Test setting unique fields
        set_unique_fields(
            (c, (UNIQUE_J,), [(UNIQUE_K, UNIQUE_L)]),
            (d, (UNIQUE_G,), [(UNIQUE_H, UNIQUE_I)]),
        )

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A, B, C
        # │
        # │ Show that unique fields are specifically NOT checked upward if not inherited
        # └─────────────────────────────────────────────────────────────────────────────

        class A(PyOb):
            """A PyOb test class"""

            # Define init method
            def __init__(
                self,
                unique_1,
                unique_2,
                unique_3,
                unique_4,
                unique_5,
                unique_6,
                unique_7,
                unique_8,
                unique_9,
            ):

                # Set unique fields
                self.unique_1 = unique_1
                self.unique_2 = unique_2
                self.unique_3 = unique_3

                self.unique_4 = unique_4
                self.unique_5 = unique_5
                self.unique_6 = unique_6

                self.unique_7 = unique_7
                self.unique_8 = unique_8
                self.unique_9 = unique_9

            # Define PyOb Meta
            class PyObMeta:

                # Define unique fields
                unique = ("unique_1", ("unique_2", "unique_3"))

        class B(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define unique fields
                unique = ("unique_4", ("unique_5", "unique_6"))

        class C(A):
            """A PyOb test class"""

            # Define PyOb Meta
            class PyObMeta:

                # Define unique fields
                unique = ("unique_7", ("unique_8", "unique_9"))

        # Here, all classes have the same fields but different unique definitions

        # Define assertDuplicateValue helper
        def assertDuplicateValue(Class, *args):

            # Initialize assertRaises block
            with self.assertRaises(UnicityError):

                # Try to initialize instance
                Class(*args)

        # Create A instance
        A("a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1")

        # Assert that unique 1 is enforced
        assertDuplicateValue(
            A, "a1", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Assert that unique 2 and unique 3 are enforced
        assertDuplicateValue(
            A, UNIQUE, "b1", "c1", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Create B instance where b.unique_4 == a.unique_1
        # There should be no conflict since unique_4 is not unique for A
        B("a2", "b2", "c2", "a1", "e2", "f2", "g2", "h2", "i2")

        # Create B instance where b.unique_5 and b.unique_6 == a.unique_2 and a.unique_3
        # There should be no conflict since unique_5 and unique_6 are not unique for A
        B("a3", "b3", "c3", "d3", "b1", "c1", "g3", "h3", "i3")

        # Assert that unique 1 is still enforced on B
        assertDuplicateValue(
            B, "a1", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Assert that unique 2 and unique 3 are still enforced on B
        assertDuplicateValue(
            B, UNIQUE, "b1", "c1", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Assert that unique 4 is enforced on B
        assertDuplicateValue(
            B, UNIQUE, UNIQUE, UNIQUE, "d3", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Assert that unique 5 and unique 6 are enforced on B
        assertDuplicateValue(
            B, UNIQUE, UNIQUE, UNIQUE, UNIQUE, "e2", "f2", UNIQUE, UNIQUE, UNIQUE
        )

        # Create C instance where c.unique_4 and c.unique_7 == a.unique_1
        # There should be no conflict with A since unique_4 and 7 are not unique for A
        # There should be no conflict with B.unique_4 since C does not inherit from B
        C("a4", "b4", "c4", "a1", "e4", "f4", "a1", "h4", "i4")

        # Create C instance where c.unique_4 and c.unique_7 == b.unique_4
        # There should be no conflict since C does not inherit from B
        C("a5", "b5", "c5", "d3", "e5", "f5", "d3", "h5", "i5")

        # Create C instance where (c.unique_5 and c.unique_6) and
        # (c.unique_8 and c.unique_9) == a.unique_2 and a.unique_3
        # There should be no conflict since (5 and 6) and (8 and 9) are not unique for A
        C("a6", "b6", "c6", "d6", "b1", "c1", "g6", "b1", "c1")

        # Create C instance where (c.unique_5 and c.unique_6) and
        # (c.unique_8 and c.unique_9) == b.unique_5 and b.unique_6
        # There should be no conflict since C does not inherit from B
        C("a7", "b7", "c7", "d7", "e2", "f2", "g7", "e2", "f2")

        # Assert that unique 1 is still enforced on C
        assertDuplicateValue(
            C, "a1", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Assert that unique 2 and unique 3 are still enforced on C
        assertDuplicateValue(
            C, UNIQUE, "b1", "c1", UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE
        )

        # Assert that unique 7 is enforced on C
        assertDuplicateValue(
            C, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, "g6", UNIQUE, UNIQUE
        )

        # Assert that unique 8 and unique 9 are enforced on C
        assertDuplicateValue(
            C, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, UNIQUE, "h4", "i4"
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST STR
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_str(self):
        """Ensures that the str dunder method behaves as expected"""

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

        # Nullify display field
        _Country.PyObMeta.display = None

        # Replicate Thailand
        tha = _Country(**tha.__dict__)

        # Assert that string defaults to the first key, i.e. ISO2
        self.assertEqual(str(tha), "TH")

        # Nullify all keys
        _Country.PyObMeta.keys = None

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

        # Assert that you can pass a custom display argument
        self.assertEqual(sgp.__str__(display="iso3"), "SGP")

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CHILD
        # └─────────────────────────────────────────────────────────────────────────────

        class Child(PyOb):
            """A test class to represent the child of a parent"""

            # Define init method
            def __init__(self, parent):
                """Init Method"""

                # Set parent
                self.parent = parent

            # Define PyOb Meta
            class PyObMeta:

                # Define display field
                display = "parent"

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ A
        # └─────────────────────────────────────────────────────────────────────────────

        class A(Child):
            """A class whose string field will point to C"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ B
        # └─────────────────────────────────────────────────────────────────────────────

        class B(Child):
            """A class whose string field will point to A"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ C
        # └─────────────────────────────────────────────────────────────────────────────

        class C(Child):
            """A class whose string field will point to B"""

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
