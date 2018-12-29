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
        Form.resize(192, 231)
        Form.setAutoFillBackground(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.loadMicroscopeBtn = QtWidgets.QPushButton(Form)
        self.loadMicroscopeBtn.setObjectName("loadMicroscopeBtn")
        self.verticalLayout.addWidget(self.loadMicroscopeBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.liveToggleBtn = QtWidgets.QPushButton(Form)
        self.liveToggleBtn.setObjectName("liveToggleBtn")
        self.verticalLayout.addWidget(self.liveToggleBtn)
        self.snapshotBtn = QtWidgets.QPushButton(Form)
        self.snapshotBtn.setObjectName("snapshotBtn")
        self.verticalLayout.addWidget(self.snapshotBtn)
        self.cameraRadBtn = QtWidgets.QRadioButton(Form)
        self.cameraRadBtn.setObjectName("cameraRadBtn")
        self.verticalLayout.addWidget(self.cameraRadBtn)
        self.eyepieceRadBtn = QtWidgets.QRadioButton(Form)
        self.eyepieceRadBtn.setObjectName("eyepieceRadBtn")
        self.verticalLayout.addWidget(self.eyepieceRadBtn)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.epiToggleBtn = QtWidgets.QPushButton(Form)
        self.epiToggleBtn.setObjectName("epiToggleBtn")
        self.horizontalLayout_2.addWidget(self.epiToggleBtn)
        self.diaToggleBtn = QtWidgets.QPushButton(Form)
        self.diaToggleBtn.setObjectName("diaToggleBtn")
        self.horizontalLayout_2.addWidget(self.diaToggleBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "deepthought"))
        self.loadMicroscopeBtn.setText(_translate("Form", "Load Microscope"))
        self.liveToggleBtn.setText(_translate("Form", "Live"))
        self.snapshotBtn.setText(_translate("Form", "Snap"))
        self.cameraRadBtn.setText(_translate("Form", "Camera"))
        self.eyepieceRadBtn.setText(_translate("Form", "Eye Piece"))
        self.epiToggleBtn.setText(_translate("Form", "EPI"))
        self.diaToggleBtn.setText(_translate("Form", "DIA"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

