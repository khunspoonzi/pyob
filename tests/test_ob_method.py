# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

import unittest

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob import PyOb

from tests.test_cases.pyob import PyObFixtureTestCase


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB METHOD TEST CASE
# └─────────────────────────────────────────────────────────────────────────────────────


class ObMethodTestCase(PyObFixtureTestCase):
    """Ob Method Test Case"""

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST LOCALIZED
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_localized(self):
        """Ensures that the Localized class method behaves as expected"""

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ COUNTRY
        # └─────────────────────────────────────────────────────────────────────────────

        # Get Country
        Country = self.Country

        # Assert that Country global store has 250 Country instances
        self.assertIsObStore(Country.obs, count=250)

        # Localize Country
        _Country = Country.Localized()

        # Assert that Country local store has 0 Country instances
        self.assertIsObStore(_Country.obs, count=0)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ VEHICLE
        # └─────────────────────────────────────────────────────────────────────────────

        class Vehicle(PyOb):
            """A PyOb class representing vehicle objects"""

        class TwoWheelVehicle(Vehicle):
            """A PyOb class representing two-wheel vehicle objects"""

        class MotorizedVehicle(Vehicle):
            """A PyOb class representing motorized vehicle objects"""

        class FourWheelVehicle(Vehicle):
            """A PyOb class representing four-wheel vehicle objects"""

        class Bicycle(TwoWheelVehicle):
            """A PyOb class representing bicycle objects"""

        class Motorcycle(TwoWheelVehicle, MotorizedVehicle):
            """A PyOb class representing motorcycle objects"""

        class Car(FourWheelVehicle, MotorizedVehicle):
            """A PyOb class representing car objects"""

        # Localize vehicle classes
        _Vehicle, _Bicycle, _Motorcycle, _Car = Vehicle.Localized(
            include=[Bicycle, Motorcycle, Car]
        )

        # Get localized TwoWheelVehicle class
        _TwoWheelVehicle = [
            base for base in _Bicycle.__bases__ if base.__name__ == "TwoWheelVehicle"
        ][0]

        # Get localized FourWheelVehicle class
        _FourWheelVehicle = [
            base for base in _Car.__bases__ if base.__name__ == "FourWheelVehicle"
        ][0]

        # Get localized MotorizedVehicle class
        _MotorizedVehicle = [
            base
            for base in _Motorcycle.__bases__
            if base.__name__ == "MotorizedVehicle"
        ][0]

        # Assert that localized Bicycle and Motorcycle share a TwoWheelVehicle base
        self.assertTrue(
            _TwoWheelVehicle.__name__ == "TwoWheelVehicle"
            and _TwoWheelVehicle in _Motorcycle.__bases__
        )

        # Assert that localized Motorcycle and Car share a MotorizedVehicle base
        self.assertTrue(
            _MotorizedVehicle.__name__ == "MotorizedVehicle"
            and _MotorizedVehicle in _Car.__bases__
        )

        # Assert that localized Car is a subclass of localized FourWheelVehicle
        self.assertTrue(issubclass(_Car, _FourWheelVehicle))

        # Iterate over global and local classes
        for Parent, Children in (
            (Vehicle, (Bicycle, Motorcycle, Car)),
            (_Vehicle, (_Bicycle, _Motorcycle, _Car)),
        ):

            # Assert that Bicycle, Motorcycle, and Car are all subclasses of Vehicle
            self.assertTrue(issubclass(Child, Parent) for Child in Children)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ REFERENCE CHECKS
        # └─────────────────────────────────────────────────────────────────────────────

        # Iterate over localized PyOb classes
        for Class, ClassLocalized in (
            (Country, _Country),
            (Vehicle, _Vehicle),
            (TwoWheelVehicle, _TwoWheelVehicle),
            (FourWheelVehicle, _FourWheelVehicle),
            (MotorizedVehicle, _MotorizedVehicle),
            (Bicycle, _Bicycle),
            (Motorcycle, _Motorcycle),
            (Car, _Car),
        ):

            # Assert that localized class is a different reference
            self.assertNotEqual(Class, ClassLocalized)

            # Assert that localized class store is a different reference
            self.assertNotEqual(id(Class._store), id(ClassLocalized._store))

            # Iterate over store indices
            for index, _index in (
                (Class._store._obs, ClassLocalized._store._obs),
                (Class._store._obs_by_key, ClassLocalized._store._obs_by_key),
                (
                    Class._store._obs_by_unique_field,
                    ClassLocalized._store._obs_by_unique_field,
                ),
            ):

                # Assert that localized index has not objects
                self.assertEqual(len(_index), 0)

                # Assert that global and local indices are separate references
                self.assertNotEqual(id(index), id(_index))

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ TEST SET
    # └─────────────────────────────────────────────────────────────────────────────────

    def test_set(self):
        """Ensures that the Set class method behaves as expected"""

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
