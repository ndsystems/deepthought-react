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
        self.ui.loadMicroscopeBtn.clicked.connect(self.load_microscope)
        self.ui.unloadBtn.clicked.connect(self.unload_microscope)
        self.ui.eyepieceRadBtn.clicked.connect(self.eyepiece_toogle)
        self.ui.snapshotBtn.clicked.connect(self.snap_image)
        self.ui.liveToggleBtn.clicked.connect(self.live)

    def snap_image(self):
        img = controls.snap_image(self.mmc, exposure_time=200)
        self.ui.widget.canvas.ax.imshow(img, cmap="gray")
        self.ui.widget.canvas.draw()

    def live(self):
        pass

    def load_microscope(self):
        if self.mmc is None:
            self.mmc = controls.loadDevices("configs/Bright_Star.cfg")
            self.mmc.initializeAllDevices()
            self.ui.loadMicroscopeBtn.setEnabled(False)
            self.ui.unloadBtn.setEnabled(True)

    def unload_microscope(self):
        self.mmc.reset()
        self.mmc = None
        self.ui.unloadBtn.setEnabled(False)
        self.ui.loadMicroscopeBtn.setEnabled(True)

    def epi_toggle(self):
        if self.epiShutter is 0:
            self.epiShutter = 1
            controls.shutter_control(self.mmc, "epi", self.epiShutter)
            self.ui.epiToggleBtn.setText("ON")

        else:
            self.epiShutter = 0
            controls.shutter_control(self.mmc, "epi", self.epiShutter)
            self.ui.epiToggleBtn.setText("EPI")

    def dia_toggle(self):
        if self.diaShutter is 0:
            self.diaShutter = 1
            controls.shutter_control(self.mmc, "dia", self.diaShutter)
            self.ui.diaToggleBtn.setText("ON")

        else:
            self.diaShutter = 0
            controls.shutter_control(self.mmc, "dia", self.diaShutter)
            self.ui.diaToggleBtn.setText("DIA")

    def eyepiece_toogle():
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = mainwindow()
    application.Form.show()
    sys.exit(app.exec_())
