# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testing.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(192, 182)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.live_toggle_btn = QtWidgets.QPushButton(Form)
        self.live_toggle_btn.setObjectName("live_toggle_btn")
        self.verticalLayout.addWidget(self.live_toggle_btn)
        self.snapshot_btn = QtWidgets.QPushButton(Form)
        self.snapshot_btn.setObjectName("snapshot_btn")
        self.verticalLayout.addWidget(self.snapshot_btn)
        self.camera_btn = QtWidgets.QRadioButton(Form)
        self.camera_btn.setObjectName("camera_btn")
        self.verticalLayout.addWidget(self.camera_btn)
        self.eyepiece_btn = QtWidgets.QRadioButton(Form)
        self.eyepiece_btn.setObjectName("eyepiece_btn")
        self.verticalLayout.addWidget(self.eyepiece_btn)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.epi_shutter_toggle_btn = QtWidgets.QPushButton(Form)
        self.epi_shutter_toggle_btn.setObjectName("epi_shutter_toggle_btn")
        self.horizontalLayout_2.addWidget(self.epi_shutter_toggle_btn)
        self.dia_shutter_toggle_btn = QtWidgets.QPushButton(Form)
        self.dia_shutter_toggle_btn.setObjectName("dia_shutter_toggle_btn")
        self.horizontalLayout_2.addWidget(self.dia_shutter_toggle_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "deepthought"))
        self.live_toggle_btn.setText(_translate("Form", "Live"))
        self.snapshot_btn.setText(_translate("Form", "Snap"))
        self.camera_btn.setText(_translate("Form", "Camera"))
        self.eyepiece_btn.setText(_translate("Form", "Eye Piece"))
        self.epi_shutter_toggle_btn.setText(_translate("Form", "EPI"))
        self.dia_shutter_toggle_btn.setText(_translate("Form", "DIA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

