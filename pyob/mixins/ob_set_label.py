# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ OB SET LABEL MIXIN
# └─────────────────────────────────────────────────────────────────────────────────────


class ObSetLabelMixin:
    """ A mixin class for PyOb object set label methods """

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LABEL SINGULAR
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def label_singular(self):
        """ Returns a singular label for the object set """

        # Determine if object set is mixed
        is_mixed = self.count() > 1 and self._Ob is None

        # Get object label
        ob_label = "Mixed" if is_mixed else self.ob_label_singular

        # Return singular label
        return self.__class__.__name__.replace("Ob", ob_label + " ")

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ LABEL PLURAL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def label_plural(self):
        """ Returns a plural label for the object set """

        # Return plural label
        return self.label_singular + "s"

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OB LABEL SINGULAR
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def ob_label_singular(self):
        """ Returns a singular label based on related object if any """

        # Return singular label
        return (self._Ob and self._Ob.label_singular) or "Ob"

    # ┌─────────────────────────────────────────────────────────────────────────────────
    # │ OB LABEL PLURAL
    # └─────────────────────────────────────────────────────────────────────────────────

    @property
    def ob_label_plural(self):
        """ Returns a plural label based on related object if any """

        # Return plural label
        return (self._Ob and self._Ob.label_plural) or "Obs"
