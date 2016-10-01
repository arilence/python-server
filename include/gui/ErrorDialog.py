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

