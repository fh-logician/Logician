import sys

from PyQt5 import QtGui, QtWidgets

from tree import Tree


# # # # # # # # # # # # # # # # # # # #
# App Class / Window Geometry
# # # # # # # # # # # # # # # # # # # #


class Logician(QtWidgets.QApplication):
    """A PyQt Application to allow a user to type in a boolean expression
    with variables of varying lengths.
    For example, a variable can be a single letter or a word
    """

    COURIER_NEW = QtGui.QFont("courier new")

    def __init__(self, *args):
        super().__init__(*args)

        # Setup the application's window
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle("Logician")
        self.setup()

        # Setup the labels for the expression and simplified fields
        self.expression_label = QtWidgets.QLabel("Expression", self.window)
        self.expression_label.setAccessibleName("Expression Label")

        self.simplified_minterm_label = QtWidgets.QLabel("Simplified Minterm", self.window)
        self.simplified_minterm_label.setAccessibleName("Simplified Minterm Label")

        self.simplified_maxterm_label = QtWidgets.QLabel("Simplified Maxterm", self.window)
        self.simplified_maxterm_label.setAccessibleName("Simplified Maxterm Label")

        # Setup the text fields for the expression, the simplified fields, and the truth table
        self.expression_text = QtWidgets.QLineEdit(self.window)
        self.expression_text.textEdited.connect(self.on_edit)
        self.expression_text.setToolTip("The boolean expression to evaluate.")
        self.expression_text.setAccessibleName("Expression text field")
        self.expression_text.setAccessibleDescription("The boolean expression to evaluate.")

        self.simplified_minterm_text = QtWidgets.QLineEdit(self.window)
        self.simplified_minterm_text.setReadOnly(True)
        self.simplified_minterm_text.setToolTip("The expression simplified as a Minterm expression.")

        self.simplified_maxterm_text = QtWidgets.QLineEdit(self.window)
        self.simplified_maxterm_text.setReadOnly(True)
        self.simplified_maxterm_text.setToolTip("The expression simplified as a Maxterm expression.")

        self.truth_table_text = QtWidgets.QTextEdit(self.window)
        self.truth_table_text.setReadOnly(True)
        self.truth_table_text.setToolTip("The truth table of the simplest expression.")

        # Setup the layout for the window
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.expression_label, 0, 0)
        self.layout.addWidget(self.expression_text, 0, 1)
        self.layout.addWidget(self.simplified_minterm_label, 1, 0)
        self.layout.addWidget(self.simplified_minterm_text, 1, 1)
        self.layout.addWidget(self.simplified_maxterm_label, 2, 0)
        self.layout.addWidget(self.simplified_maxterm_text, 2, 1)
        self.layout.addWidget(self.truth_table_text, 4, 0, 2, 4)

        # Add the layout to a widget and set the central widget of this
        #   application to said widget
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.window.setCentralWidget(widget)
        self.window.show()  # show the window
        sys.exit(self.exec_())

    def setup(self):

        # Setup the window geometry to center the app on the screen
        #   first retrieve the app's dimensions
        screen_resolution = self.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.window.setGeometry(
            # This will set the XY coordinates to offset the width and height of the window
            #   to center the window on whichever screen is being used
            (width - width // 2) // 2, (height - height // 2) // 2,
            width // 2, height // 2  # The window size will be half the width and half the height of the screen
        )

    def on_edit(self):
        """This function is called whenever the Expression textfield is changed by the user
        """

        self.simplified_maxterm_label.setStyleSheet("color: #000000;")
        self.simplified_minterm_label.setStyleSheet("color: #000000;")

        # Try to evaluate the expression and set the simplified fields
        #   and the truth table
        try:
            tree = Tree(self.expression_text.text())
            minterm = tree.simplify(get_minterm=True)
            maxterm = tree.simplify(get_minterm=False)
            self.simplified_minterm_text.setText(str(minterm))
            self.simplified_maxterm_text.setText(str(maxterm))

            # Highlight the shortest expression by comparing the sizes of
            #   the minterm expression and maxterm expression
            if len(str(minterm)) < len(str(maxterm)):
                self.simplified_minterm_label.setStyleSheet("color: #00AA00;")
                self.truth_table_text.setText(minterm.get_table())
            else:
                self.simplified_maxterm_label.setStyleSheet("color: #00AA00;")
                self.truth_table_text.setText(maxterm.get_table())
            self.truth_table_text.setFont(Logician.COURIER_NEW)

        # If there is an error, don't set the fields to anything
        except ValueError as _:
            self.simplified_minterm_text.setText("")
            self.simplified_maxterm_text.setText("")
            self.truth_table_text.setText("")


if __name__ == "__main__":
    QtWidgets.QApplication.setStyle('fusion')
    logician = Logician(sys.argv)
    QtWidgets.QApplication.setStyle('fusion')
