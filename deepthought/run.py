from PyQt5 import QtWidgets
from gui import main
import controls
import sys


class mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        self.Form = QtWidgets.QWidget()
        self.ui = main.Ui_Form()
        self.ui.setupUi(self.Form)
        self.mmc = None
        self.epiShutter = 0
        self.diaShutter = 0
        self.ui.epiToggleBtn.clicked.connect(self.epi_toggle)
        self.ui.diaToggleBtn.clicked.connect(self.dia_toggle)

    def load_microscope(self):
        if self.mmc is None:
            self.mmc = controls.loadDevices()
        else:
            pass

    def epi_toggle(self):
        if self.epiShutter is 0:
            self.epiShutter = 1
            controls.shutter_control(mmc, "epi", self.epiShutter)
            self.ui.epiToggleBtn.setText("ON")

        else:
            self.epiShutter = 0
            controls.shutter_control(mmc, "epi", self.epiShutter)
            self.ui.epiToggleBtn.setText("EPI")

    def dia_toggle(self):
        if self.diaShutter is 0:
            self.diaShutter = 1
            controls.shutter_control(mmc, "dia", self.epiShutter)
            self.ui.diaToggleBtn.setText("ON")

        else:
            self.diaShutter = 0
            controls.shutter_control(mmc, "dia", self.epiShutter)
            self.ui.diaToggleBtn.setText("DIA")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = mainwindow()
    application.Form.show()
    sys.exit(app.exec_())
