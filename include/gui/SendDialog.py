"""---------------------------------------------------------------------------------------
--      SOURCE FILE:        SendDialog.py - Simple dialog box to specify files
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
--      This file extends the PYQT dialog class to build a dialog box with a text field,
--      file browser button, submit button, and cancel button. The file browser button
--      displays the system file browser and allows the user to select a file. Once a
--      file has been selected, the destination is populated in the text field. When a
--      user presses the submit button, the values are saved and can be retrieved later.
--      If the user presses the cancel button, no values are saved and progress is reset.
---------------------------------------------------------------------------------------"""
from PyQt4 import QtGui
from PyQt4.QtGui import *

class SendDialog(QDialog):
    DIALOG_HEIGHT = 100
    DIALOG_WIDTH = 450

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.fileLocation = ""
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
        self.setWindowTitle("Browse For A File")
        self.setGeometry(100, 100, SendDialog.DIALOG_WIDTH, SendDialog.DIALOG_HEIGHT)

        self.browseText = QLineEdit(self)

        browseBTN = QPushButton(self)
        browseBTN.setText("Browse")
        browseBTN.clicked.connect(self.openBrowser)

        cancelBTN = QPushButton(self)
        cancelBTN.setText("Cancel")
        cancelBTN.clicked.connect(self.cancelBrowse)

        acceptBTN = QPushButton(self)
        acceptBTN.setText("Send File")
        acceptBTN.clicked.connect(self.acceptBrowse)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.browseText)
        hbox.addWidget(browseBTN)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(cancelBTN)
        hbox2.addWidget(acceptBTN)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def openBrowser(self):
        self.fileLocation = QtGui.QFileDialog.getOpenFileName(self)
        self.browseText.setText(self.fileLocation)

    def acceptBrowse(self):
        self.accept()

    def cancelBrowse(self):
        self.close()

