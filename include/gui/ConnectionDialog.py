from PyQt4 import QtGui
from PyQt4.QtGui import *

class ConnectionDialog(QDialog):
    DIALOG_HEIGHT = 100
    DIALOG_WIDTH = 450

    def __init__(self, remoteHost, remotePort, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.remoteHost = remoteHost
        self.remotePort = remotePort
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
        self.setWindowTitle("File Transfer App - Server Connection")
        self.setGeometry(100, 100, ConnectionDialog.DIALOG_WIDTH, ConnectionDialog.DIALOG_HEIGHT)

        hostLabel = QLabel(self)
        hostLabel.setText("Enter Host Address")

        self.hostText = QLineEdit(self)
        self.hostText.setText(self.remoteHost)

        connectBTN = QPushButton(self)
        connectBTN.setText("Connect")
        connectBTN.clicked.connect(self.acceptConnect)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.hostText)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addStretch(1)
        hbox2.addWidget(connectBTN)

        vbox = QVBoxLayout()
        vbox.addWidget(hostLabel)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def acceptConnect(self):
        self.remoteHost = self.hostText.text()
        self.accept()

