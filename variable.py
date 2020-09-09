class Variable:
    """A LogicVar class holds information about a variable, or a literal, in a boolean algebraic
    expression of logical expression.

    :param value: The variable letter for this Variable object
    :param has_not: Whether or not this Variable object has a ~ (NOT) operator attached to it
    :param json: A JSON object to load a Variable object from.
        The required keys are the same as the parameters (value, has_not)

    :type value: str
    :type has_not: bool
    :type json: dict
    """

    def __init__(self, value=None, has_not=None, *, json=None):

        # Check if the JSON object is given
        if json is not None:

            # Validate that value and has_not keys are given
            if "value" in json and "has_not" in json:
                value = json["value"]
                has_not = json["has_not"]
            else:
                raise KeyError("The \"value\" and \"has_not\" keys must exist in the LogicVar JSON.")

        # Make sure value and has_not exist
        if value is not None and has_not is not None:
            self.__value = value
            self.__has_not = has_not
        else:
            raise ValueError("The \"value\" and \"has_not\" parameters must not be a NoneType.")

    def __str__(self):
        return "{}{}".format(
            "NOT " if self.has_not() else "",
            self.get_value()
        )

    # # # # # # # # # # # # # # # # # # # # # # # # #
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_value(self) -> str:
        """Returns the variable letter of this LogicVar object"""
        return self.__value

    def has_not(self) -> bool:
        """Returns whether or not this LogicVar object has a ~ (NOT) operator attached to it"""
        return self.__has_not

    # # # # # # # # # # # # # # # # # # # # # # # # #
    # Evaluation Methods
    # # # # # # # # # # # # # # # # # # # # # # # # #

    def evaluate(self, truth_values) -> bool:
        """Evaluates this LogicVar object given a dict of truth values that include the letter

        :param truth_values: A JSON object of truth values for this Variable object to use to evaluate
        :type truth_values: dict
        """
        if self.has_not():
            return not truth_values[self.get_value()]
        return truth_values[self.get_value()]

    def functional(self) -> str:
        """Returns a functional representation of this Variable

        For example:
            - ``NOT a`` would be functionally equivalent to ``not(a)``
        """
        expr = f"{self.get_value()}"
        if self.has_not():
            expr = f"not({expr})"
        return expr