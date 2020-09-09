class BoolExpr:
    def __init__(self, has_not = False):
        """A BoolExpr is an abstract class that identifies either a Variable
        or an Expression that is used in a Boolean Expression

        :param has_not: Whether or not this BoolExpr has a NOT operator attached to it
        :type has_not: bool
        """
        self.__has_not = has_not

    # # # # # # # # # # # # # # # # # # # # # # # # #
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # #

    def has_not(self) -> bool:
        """Returns whether or not this BoolExpr has a ``NOT`` operator attached to it"""
        return self.__has_not

    # # # # # # # # # # # # # # # # # # # # # # # # #
    # Evaluation Methods
    # # # # # # # # # # # # # # # # # # # # # # # # #

    def evaluate(self, truth_values: dict) -> bool:
        """Evaluates this BoolExpr given a JSON object of truth values
        to evaluate with.

        :param truth_values: A JSON object of truth values for each variable
            in a boolean expression to evaluate against.
        :return: The resulting boolean evaluation
        """
        raise NotImplementedError("The evaluation method must be implemented")

    def functional(self) -> str:
        """Returns a functional representation of this BoolExpr

        For example:
            - ``NOT a`` would become ``not(a)``
            - ``NOT a OR b AND c`` would become ``or(not(a), and(b, c))``
        """
        raise NotImplementedError("The functional method must be implemented")

