# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(192, 182)
        Form.setAutoFillBackground(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.LiveToggleBtn = QtWidgets.QPushButton(Form)
        self.LiveToggleBtn.setObjectName("LiveToggleBtn")
        self.verticalLayout.addWidget(self.LiveToggleBtn)
        self.SnapshotBtn = QtWidgets.QPushButton(Form)
        self.SnapshotBtn.setObjectName("SnapshotBtn")
        self.verticalLayout.addWidget(self.SnapshotBtn)
        self.CameraRadBtn = QtWidgets.QRadioButton(Form)
        self.CameraRadBtn.setObjectName("CameraRadBtn")
        self.verticalLayout.addWidget(self.CameraRadBtn)
        self.EyepieceRadBtn = QtWidgets.QRadioButton(Form)
        self.EyepieceRadBtn.setObjectName("EyepieceRadBtn")
        self.verticalLayout.addWidget(self.EyepieceRadBtn)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.EpiToggleBtn = QtWidgets.QPushButton(Form)
        self.EpiToggleBtn.setObjectName("EpiToggleBtn")
        self.horizontalLayout_2.addWidget(self.EpiToggleBtn)
        self.DiaToggleBtn = QtWidgets.QPushButton(Form)
        self.DiaToggleBtn.setObjectName("DiaToggleBtn")
        self.horizontalLayout_2.addWidget(self.DiaToggleBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "deepthought"))
        self.LiveToggleBtn.setText(_translate("Form", "Live"))
        self.SnapshotBtn.setText(_translate("Form", "Snap"))
        self.CameraRadBtn.setText(_translate("Form", "Camera"))
        self.EyepieceRadBtn.setText(_translate("Form", "Eye Piece"))
        self.EpiToggleBtn.setText(_translate("Form", "EPI"))
        self.DiaToggleBtn.setText(_translate("Form", "DIA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

