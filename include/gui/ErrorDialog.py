"""---------------------------------------------------------------------------------------
--      SOURCE FILE:        ErrorDialog.py - Simple dialog box to show error messages
--
--      PROGRAM:            file_transport
--
--      DATE:               October 2, 2016
--
--      REVISION:           (Date and Description)
--
--      DESIGNERS:          Anthony Smith
--
--      PROGRAMMERS:        Anthony Smith
--
--      NOTES:
--      This file extends the PYQT dialog class to build a dialog box with a text label
--      and button. The label is set to the value passed in during construction. The
--      value is meant to be an error message that is displayed to the user. Once the
--      user reads the message, clicking the button will dismiss the error message.
---------------------------------------------------------------------------------------"""
from PyQt4 import QtGui
from PyQt4.QtGui import *

class ErrorDialog(QDialog):
    DIALOG_HEIGHT = 100
    DIALOG_WIDTH = 450

    def __init__(self, errorText, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.errorText = errorText
        self.setupUi()
        self.centerPosition()

    def centerPosition(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.show()

    def setupUi(self):
        self.setWindowTitle("Uh Oh! ERROR!")
        self.setGeometry(100, 100, ErrorDialog.DIALOG_WIDTH, ErrorDialog.DIALOG_HEIGHT)

        errorLabel = QLabel(self)
        errorLabel.setText(self.errorText)

        closeBTN = QPushButton(self)
        closeBTN.setText("Close")
        closeBTN.clicked.connect(self.closeDialog)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(closeBTN)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(errorLabel)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def closeDialog(self):
        self.close()

