from PyQt4 import QtGui
from PyQt4.QtGui import *

class GetDialog(QDialog):
    DIALOG_HEIGHT = 100
    DIALOG_WIDTH = 450

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.fileName = ""
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
        self.setWindowTitle("Enter File Name")
        self.setGeometry(100, 100, GetDialog.DIALOG_WIDTH, GetDialog.DIALOG_HEIGHT)

        self.fileNameText = QLineEdit(self)

        cancelBTN = QPushButton(self)
        cancelBTN.setText("Cancel")
        cancelBTN.clicked.connect(self.cancelInput)

        acceptBTN = QPushButton(self)
        acceptBTN.setText("Get File")
        acceptBTN.clicked.connect(self.acceptInput)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cancelBTN)
        hbox.addWidget(acceptBTN)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.fileNameText)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def acceptInput(self):
        self.fileName = self.fileNameText.text()
        self.accept()

    def cancelInput(self):
        self.fileName = ""
        self.close()

