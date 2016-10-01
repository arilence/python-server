from PyQt4 import QtGui
from PyQt4.QtGui import *

class SendDialog(QDialog):
    DIALOG_HEIGHT = 100
    DIALOG_WIDTH = 450

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.fileLocation = ""
        self.setupUi()

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

