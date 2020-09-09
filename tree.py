from expression import Expression
from lark import Lark
from lark.tree import Tree as LarkTree
from qm import QM
from typing import Union
from variable import Variable


class Tree:

    BOOLEAN = Lark(
        """
        start: orexpr
        ?orexpr: (orexpr ("+" | "|" ~ 1..2 | "or" | "OR"))? andexpr
        ?andexpr: (andexpr ("*" | "&" ~ 1..2 | "and" | "AND"))? xorexpr
        ?xorexpr: (xorexpr ("^" | "xor" | "XOR"))? xnorexpr
        ?xnorexpr: (xnorexpr ("-^" | "xnor" | "XNOR"))? norexpr
        ?norexpr: (norexpr ("-+" | "nor" | "NOR"))? nandexpr
        ?nandexpr: (nandexpr ("-*" | "nand" | "NAND"))? term
        ?term: nexpr
            | pexpr
            | IDENT
        ?nexpr: TILDE orexpr
        ?pexpr: "(" orexpr ")"
            | "[" orexpr "]"
        TILDE: "~" | "!" | "not" | "NOT"

        %import common.CNAME -> IDENT
        %import common.WS
        %ignore WS
        """
    )

    @staticmethod
    def __create_dict(parse_tree) -> tuple:
        """Creates a parsable JSON object that can be parsed through LogicNode and LogicVar
        objects to be used to represent a boolean expression

        :param parse_tree: A Lark grammar tree object to parse through
        :type parse_tree: lark.tree.Tree

        :return: A tuple containing the parsed expression as a JSON object and a list of variables the expression
        :rtype: tuple
        """

        variables = []

        # Check if the parse_tree is a Tree
        if isinstance(parse_tree, LarkTree):

            # Check if the expression is an orexpr (OR) or andexpr (AND)
            if parse_tree.data != "nexpr":

                # Get the left and right expression along with any new variables that may exist
                left, variables_new_left = Tree.__create_dict(parse_tree.children[0])
                right, variables_new_right = Tree.__create_dict(parse_tree.children[1])
                for variable in variables_new_left + variables_new_right:
                    if variable not in variables:
                        variables.append(variable)

                # Return the expression and the variables
                return {
                           "left": left,
                           "operator": parse_tree.data[: parse_tree.data.find("expr")].upper(),
                           "right": right,
                           "has_not": False
                       }, variables

            # Check if the expression is an nexpr (NOT)
            else:

                # Get the expression along with any new variables that may exist
                expression, variables_new = Tree.__create_dict(parse_tree.children[1])
                expression["has_not"] = not expression["has_not"]
                for variable in variables_new:
                    if variable not in variables:
                        variables.append(variable)

                # Return the expression and the variables
                return expression, variables

        # The parse_tree is an ident (Variable)
        return {
                   "value": parse_tree.value,
                   "has_not": False
               }, [parse_tree.value]

    def __init__(self, expr: str):

        # Try to parse the expression
        try:
            self.__root, self.__variables = Tree.__create_dict(
                Tree.BOOLEAN.parse(expr).children[0]  # This ignores the "start" Tree
            )
            self.__variables.sort()

            # Check if the expression is a LogicNode or LogicVar
            if "value" in self.__root:
                self.__root = Variable(json = self.__root)
            else:
                self.__root = Expression(json = self.__root)

        # If parsing the expression fails, the boolean expression is invalid
        except:
            raise ValueError("The expression given is invalid")

    def __str__(self):
        return str(self.__root)

    # # # # # # # # # # # # # # # # # # # #
    # Getters
    # # # # # # # # # # # # # # # # # # # #

    def get_variables(self) -> list:
        """Returns a list of variables used in this Tree"""
        return self.__variables

    def get_table(self, as_list: bool = False) -> Union[str, list]:
        """Returns a truth table of the root expression of this Tree

        :param as_list: Whether or not to return the truth table as a list of lines
        :type as_list: bool
        """

        # Create the header row which holds the variables and result like the following:
        #   | a | b | c | (a * b) + c |
        header = "| {} | {} |".format(
            " | ".join(self.get_variables()),
            str(self)
        )

        # Create the separator row which uses symbols to look like the following:
        #   +---+---+---+-------------+
        separator = "+-{}-+-{}-+".format(
            "-+-".join([
                "-" * len(var)
                for var in self.get_variables()
            ]),
            "-" * len(str(self))
        )

        # Create the truth values and their evaluations which just consists of 1's and 0's
        #   to look like the following:
        #   | 0 | 1 | 0 |      0      |
        evaluations = self.evaluate()
        values = "\n".join([
            "| {} | {} |".format(
                " | ".join([
                    ("1" if evaluation["truth_values"][value] else "0").center(len(value))
                    for value in evaluation["truth_values"]
                ]),
                ("1" if evaluation["truth_value"] else "0").center(len(str(self)))
            )
            for evaluation in evaluations
        ])

        if as_list:
            return [ header, separator, values ]
        return f"{header}\n{separator}\n{values}"

    # # # # # # # # # # # # # # # # # # # #
    # Evaluation Methods
    # # # # # # # # # # # # # # # # # # # #

    def evaluate(self) -> list:
        """Evaluates the root of this Tree to get boolean values where the root expression
        is 1 or 0

        :return: A list of evaluations and their truth values that make up the evaluation
        """

        # Iterate through all the integer values from 2 ** len(variables)
        evaluations = []
        for binary in range(2 ** len(self.get_variables())):

            # Create a JSON object for each variable and whether or not this variable
            #   is true at the current binary value
            truth_values = {
                self.get_variables()[i]: binary & (1 << (len(self.get_variables()) - 1 - i)) != 0
                for i in range(len(self.get_variables()))
            }

            # Add the evaluation for this binary value to the list of evaluations
            evaluations.append({
                "truth_values": truth_values,
                "truth_value": self.__root.evaluate(truth_values)
            })
        return evaluations

    def simplify(self, get_minterm: bool = None) -> 'Tree':
        """Simplifies the boolean expression at the root
        and returns the most simplified expression obtained
        from either minterm or maxterm evaluation.

        :param get_minterm: Whether to get the minterm expression or maxterm expression.
            By default, the function returns the shortest of the two
        :type get_minterm: bool

        :return: The simplified boolean expression inside a Tree
        :rtype: Tree
        """

        # Get the minterm and maxterm true-at values
        #   Note that a minterm expression is true where the expression evaluates
        #   to true (1) and a maxterm expresion is true where the expression evaluates
        #   to false (0)
        evaluations = self.evaluate()
        true_at_minterms = [
            decimal
            for decimal in range(len(evaluations))
            if evaluations[decimal]["truth_value"]
        ]
        true_at_maxterms = [
            decimal
            for decimal in range(len(evaluations))
            if not evaluations[decimal]["truth_value"]
        ]

        minterm_qm = QM(self.get_variables(), true_at_minterms).get_function()
        maxterm_qm = QM(self.get_variables(), true_at_maxterms, is_maxterm = True).get_function()
        
        if get_minterm is not None:
            if get_minterm:
                return Tree(minterm_qm)
            return Tree(maxterm_qm)
        return Tree(min(minterm_qm, maxterm_qm, key = lambda qm: len(qm)))

    def functional(self) -> str:
        """Returns this Tree object in a functional notation

        For example:
            - ``a or b and c`` is functionally equivalent to ``and(or(a, b), c)``
        """
        return self.__root.functional()