from sys import exit
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)

ERROR_MSG = "ERROR"

# Define sizes in pixels.
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40


# View.
class PyCalcWindow(QMainWindow):
    """ Main UI (View). """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        centralWidget.setStyleSheet(
            'QWidget {background-color: #D8DEE9}'   # darkest snow storm
        )
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        # Default style is good.
        '''self.display.setStyleSheet(
            'border: 2px solid #ECEFF4;' # lightest snow storm
            # 'border: 2px solid #E5E9F0;' # med snow storm
        )'''
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],  # row 1
            ["4", "5", "6", "*", "("],  # row 2, etc.
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                self.buttonMap[key].setStyleSheet(
                    'QPushButton {background-color: #4C566A;'   #lighest polar night
                    'color: #E5E9F0}'   # med snow storm
                )
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """ Set display's text.  """
        self.display.setText(text)
        self.display.setFocus()     # sets cursor's focus on the display

    def displayText(self):
        """ Get display's text. """
        return self.display.text()

    def clearDisplay(self):
        """ Clear display. """
        self.setDisplayText("")

# Model.
def evaluateExpression(expression):
    """ Evaluate a math expression (Model). """
    # TODO: Catch specific exception(s).
    # TODO: Re-write this without the use of eval.
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result

# Controller.
class PyCalc(object):
    """ The app's Controller class. """
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        """ Request result and display it. """
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        """ Update expression with this subExpression and display it. """
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        """ Connects all controls. Controls either build an expression,
         evaluate the expression, or clear the display. """
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)


if __name__ == "__main__":
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    exit(pycalcApp.exec())
