# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ GENERAL IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from functools import cmp_to_key
from operator import itemgetter

# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ PROJECT IMPORTS
# └─────────────────────────────────────────────────────────────────────────────────────

from pyob.exceptions import MultipleObjectsError, ZeroObjectsError
from pyob.tools import (
    convert_obs_dict_to_list,
    filter_and,
    filter_by_key,
    filter_by_keys,
    is_ob_set,
)
from pyob.utils import Nothing


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB SET METHOD MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class ObSetMethodMixin:
    """ A mixin class for PyOb object set methods """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ APPEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def append(self, ob, distinct=False):
        """ Appends a PyOb object to a PyOb object set """

        # Return if distinct and object already in object set
        if distinct and ob in self:
            return

        # Update current instance
        self.__dict__ = (self + ob).__dict__

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ CLEAR
    # └─────────────────────────────────────────────────────────────────────────────────

    def clear(self):
        """ Clears a PyOb object set so that it is empty """

        # Set objects to empty dict
        self._obs = {}

        # Set objects by key to empty dict
        self._obs_by_key = {}

        # Set objects by unique field to empty dict
        self._obs_by_unique_field = {}

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COPY
    # └─────────────────────────────────────────────────────────────────────────────────

    def copy(self):
        """ Copies a PyOB object set into a new PyOb object set """

        # Return a copied object set
        return self.New() + self

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ COUNT
    # └─────────────────────────────────────────────────────────────────────────────────

    def count(self):
        """ Returns a count of PyOb objects in a PyOb object set """

        # Return the length of the object set
        return sum(self._obs.values())

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DIFFERENCE
    # └─────────────────────────────────────────────────────────────────────────────────

    def difference(self, obs):
        """ Returns the difference of two object sets using the - operator """

        # Return the difference of the object sets
        return self - obs

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ DISTINCT
    # └─────────────────────────────────────────────────────────────────────────────────

    def distinct(self):
        """ Returns an object set of distinct items from the current object set """

        # Return the union of an empty and the current object set
        return self.New() + set(self)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ EXTEND
    # └─────────────────────────────────────────────────────────────────────────────────

    def extend(self, obs, distinct=False):
        """ Extends the current PyOb object set by another PyOb object set """

        # Check if distinct
        if distinct:

            # Filter out objects that already exist in current object set
            obs = obs - self if is_ob_set(obs) else [o for o in obs if o not in self]

        # Update current instance
        self.__dict__ = (self + obs).__dict__

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter(self, **kwargs):
        """ Filters a PyOb object set based on a series of keyword arguments """

        # Return filtered object set
        return self.New() + filter_and(self._obs, **kwargs)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER BY KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_by_key(self, value):
        """ Filters a PyOb object set based on key """

        # Return filtered object set
        return self.New() + filter_by_key(
            self._obs, self._keys, value, ob_label_plural=self.ob_label_plural
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER BY KEYS
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_by_keys(self, *values):
        """ Filters a PyOb object set based on key """

        # Return filtered object set
        return self.New() + filter_by_keys(
            self._obs, self._keys, values, ob_label_plural=self.ob_label_plural
        )

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_first(self, **kwargs):
        """ Filters a PyOb object set and returns the first result """

        # Return first object of filtered object set
        return self.filter(**kwargs).first()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FILTER ONLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def filter_only(self, **kwargs):
        """ Filters a PyOb object set and returns the only result or error """

        # Return the only object of the filtered object set
        return self.filter(**kwargs).only()

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ FIRST
    # └─────────────────────────────────────────────────────────────────────────────────

    def first(self, n=None):
        """ Returns the first PyOb object of a PyOb object set """

        # Get objects as list
        _obs = convert_obs_dict_to_list(self._obs)

        # Return the first (n) object(s) of the object set
        return self[: n + 1] if n is not None else (_obs[0] if _obs else None)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ INTERSECTION
    # └─────────────────────────────────────────────────────────────────────────────────

    def intersection(self, obs):
        """ Returns the intersection of two object sets using the & operator """

        # Return the intersection of both object sets
        return self & obs

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEY
    # └─────────────────────────────────────────────────────────────────────────────────

    def key(self, key, default=Nothing):
        """ Returns the PyOb object associated with a key from the PyOb object set """

        # Get objects by key
        obs = self.filter_by_key(key)

        # Check if distinct object count is 1
        if obs.distinct().count() == 1:

            # Return the first and only object
            return obs.first()

        # Check if default is Nothing
        if default is Nothing:

            # Raise KeyError
            raise KeyError(key)

        # Return default
        return default

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ KEYS
    # └─────────────────────────────────────────────────────────────────────────────────

    def keys(self, *keys):
        """ Returns a PyOb object set of objects associated with a series of keys """

        # Initialize an empty object set
        obs = self.New()

        # Iterate over keys
        for key in keys:

            # Filter by key and add distinct objects to object set
            obs |= self.filter_by_key(key)

        # Return filtered object set
        return obs

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LAST
    # └─────────────────────────────────────────────────────────────────────────────────

    def last(self, n=None):
        """ Returns the last PyOb object of a PyOb object set """

        # Get objects as list
        _obs = convert_obs_dict_to_list(self._obs)

        # Return the last (n) object(s) of the object set
        return self[-n:] if n is not None else (_obs[-1] if _obs else None)

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ ONLY
    # └─────────────────────────────────────────────────────────────────────────────────

    def only(self):
        """ Returns the one and only object in an object set or raises an error """

        # Get distinct object count
        ob_count = self.distinct().count()

        # Return first and only object
        if ob_count == 1:
            return self.first()

        # Get object set name
        name = self.name

        # Get object plural label
        ob_label_plural = self.ob_label_plural.lower()

        # Check if there are multiple objects
        if ob_count > 1:

            # Raise MultipleObjectsError
            raise MultipleObjectsError(
                f"{name}.only() returned multiple {ob_label_plural}"
            )

        # Otherwise raise ZeroObjectsError
        raise ZeroObjectsError(f"{name}.only() returned zero {ob_label_plural}")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ SORT
    # └─────────────────────────────────────────────────────────────────────────────────

    def sort(self, *fields):
        """
        Sorts a PyOb object set based on a series of field arguments

        https://stackoverflow.com/questions/1143671/how-to-sort-objects-by-multiple-
            keys-in-python
        """

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ FIELDS
        # └─────────────────────────────────────────────────────────────────────────────

        # Strip fields
        fields = [field.strip() for field in fields]

        # Convert fields into signed itemgetters
        fields = [
            (
                (itemgetter(field[1:]), -1)
                if field.startswith("-")
                else (itemgetter(field), 1)
            )
            for field in fields
        ]

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ CMP
        # └─────────────────────────────────────────────────────────────────────────────

        # Define inner cmp helper function
        def cmp__(x, y):
            """ Compares the x and y values """

            # Return result
            return (x > y) - (x < y)

        # Define outer cmp helper function
        def cmp_(x, y, mult):
            """
            Replacement for built-in function cmp that was removed in Python 3

            Compare the two objects x and y and return an integer according to
            the outcome. The return value is negative if x < y, zero if x == y
            and strictly positive if x > y.

            https://portingguide.readthedocs.io/en/latest/comparisons.html
                #the-cmp-function
            """

            # Iterate over x and y
            for (value, result) in ((x, 1), (y, -1)):

                # Check if value is None
                if value is None:

                    # Return result based on sort direction
                    return mult * result

                    # NOTE: This ensures that None values are always at the end

            # Initialize try-except block
            try:

                # Return comparison of x and y
                return cmp__(x, y)

            # Handle TypeError, e.g. "foo" > 5
            except TypeError:

                # Return comparison of x and y type IDs
                return cmp__(*[id(type(val)) for val in (x, y)])

                # NOTE: We can't arbitrarily drop elements; so just sort them by type

        # Define main cmp function
        def cmp(left, right):

            # Define field iterator
            field_iter = (
                cmp_(fn(left.__dict__), fn(right.__dict__), mult) * mult
                for fn, mult in fields
            )

            # Return result
            return next((result for result in field_iter if result), 0)

        # ┌─────────────────────────────────────────────────────────────────────────────
        # │ RETURN SORTED OBJECT SET
        # └─────────────────────────────────────────────────────────────────────────────

        # Return sorted object set
        return self.New() + sorted(self._obs, key=cmp_to_key(cmp))

        # TODO: HANDLE DICT IN __ADD__
        # TODO: FieldError for non-existent fields?
        # TODO: Make sortable objects traversable

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ UNION
    # └─────────────────────────────────────────────────────────────────────────────────

    def union(self, obs):
        """ Returns the union of two object sets using the | operator """

        # Return the union of both object sets
        return self | obs
