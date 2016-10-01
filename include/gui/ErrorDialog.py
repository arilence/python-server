from PyQt4 import QtGui
from PyQt4.QtGui import *

class ErrorDialog(QDialog):
    DIALOG_HEIGHT = 100
    DIALOG_WIDTH = 450

    def __init__(self, errorText, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.errorText = errorText
        self.setupUi()

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

