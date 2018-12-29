from PyQt5 import QtWidgets
from main import Ui_Form
import sys


class mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)

        self.epiShutter = 0
        self.diaShutter = 0
        self.ui.EpiToggleBtn.clicked.connect(self.epi_toggle)
        self.ui.DiaToggleBtn.clicked.connect(self.dia_toggle)

    def epi_toggle(self):
        if self.epiShutter is 0:
            self.ui.EpiToggleBtn.setText("ON")
            self.epiShutter = 1

        else:
            self.ui.EpiToggleBtn.setText("EPI")
            self.epiShutter = 0

    def dia_toggle(self):
        if self.diaShutter is 0:
            self.ui.DiaToggleBtn.setText("ON")
            self.diaShutter = 1

        else:
            self.ui.DiaToggleBtn.setText("DIA")
            self.diaShutter = 0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = mainwindow()
    application.Form.show()
    sys.exit(app.exec_())
