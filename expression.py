from typing import Union
from variable import Variable


class Expression:
    """A Expression class holds information about a boolean expression

    :param left: The left side of this Expression
    :param operator: The operator of this Expression
    :param right: The right side of this Expression
    :param has_not: Whether or not this Expression object has a ~ (NOT) operator attached to it
    :param json: A JSON object to load an Expression object from

    :type left: Expression or Variable
    :type operator: str
    :type right: Expression or Variable
    :type has_not: bool
    :type json: dict
    """

    def __init__(self, left: ['Expression', Variable] = None,
                 operator: str = None,
                 right: ['Expression', Variable] = None,
                 has_not: bool = False, *,
                 json: dict = None):

        # Check if the JSON object is given
        if json is not None:

            # Validate that the left, operator, right, and has_not keys exist
            if "left" in json and "operator" in json and "right" in json and "has_not" in json:

                # Check if the operator is a NAND, a NOR, or an XNOR, invert the has_not
                operator = json["operator"]
                has_not = json["has_not"]
                if operator in ["NAND", "NOR", "XNOR"]:
                    has_not = not has_not

                left = Expression(json=json["left"]) if "value" not in json["left"] else Variable(json=json["left"])
                right = Expression(json=json["right"]) if "value" not in json["right"] else Variable(json=json["right"])

            # The left, operator, right, and has_not keys do not exist
            else:
                raise KeyError(
                    "The \"left\", \"operator\", \"right\", and \"has_not\" keys must exist in the Expression JSON")

        # Make sure left, operator, right, and has_not exist
        if left is not None and operator is not None and right is not None and has_not is not None:
            self.left = left
            self.operator = operator
            self.right = right
            self.has_not = has_not
        else:
            raise ValueError(
                "The \"left\", \"operator\", \"right\", and \"has_not\" parameters must not be a NoneType.")

    def __str__(self):
        if not self.has_not:
            return "({} {} {})".format(
                str(self.get_left()), self.get_operator(), str(self.get_right())
            )
        return "NOT({} {} {})".format(
            str(self.get_left()), self.get_operator(), str(self.get_right())
        )

    # # # # # # # # # # # # # # # # # # # # # # # # #
    # Getters
    # # # # # # # # # # # # # # # # # # # # # # # # #

    def get_left(self) -> Union['Expression', 'Variable']:
        """Returns the left value of this Expression object"""
        return self.left

    def get_operator(self) -> str:
        """Returns the operator of this Expression object"""
        return self.operator

    def get_right(self) -> Union['Expression', 'Variable']:
        """Returns the right value of this Expression object"""
        return self.right

    # # # # # # # # # # # # # # # # # # # # # # # # #
    # Evaluation Methods
    # # # # # # # # # # # # # # # # # # # # # # # # #

    def evaluate(self, truth_values) -> bool:
        """Evaluates this Expression object given a dict of truth values

        :param truth_values: A JSON object of truth values for this Expression object to use to evaluate
        :type truth_values: dict
        """
        left = self.get_left().evaluate(truth_values)
        right = self.get_right().evaluate(truth_values)

        evaluation = False
        if self.get_operator() in ["OR", "NOR"]:
            evaluation = left or right
        elif self.get_operator() in ["AND", "NAND"]:
            evaluation = left and right
        elif self.get_operator() in ["XOR", "XNOR"]:
            evaluation = left ^ right

        if self.has_not:
            return not evaluation
        return evaluation

    def functional(self) -> str:
        """Returns a functional representation of this Expression

        For example:
            - ``a AND b`` would be functionally equivalent to ``and(a, b)``
            - ``NOT a AND b`` would be functionally equivalent to ``and(not(a), b)``
            - ``NOT (a AND b)`` would be functionally equivalent to ``not(and(a, b))``
        """
        expr = f"{self.get_operator().lower()}({self.get_left().functional()}, {self.get_right().functional()})"
        if self.has_not:
            expr = f"not({expr})"
        return expr
