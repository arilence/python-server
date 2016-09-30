import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QPushButton

WINDOW_HEIGHT = 480
WINDOW_WIDTH = (WINDOW_HEIGHT * 16) / 9

DIALOG_HEIGHT = 220
DIALOG_WIDTH = (DIALOG_HEIGHT * 16) / 9

def window():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    w.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
    w.setWindowTitle("File Transfer App")

    b = QPushButton(w)
    b.setText("A Dialog")
    b.move(50, 20)
    b.clicked.connect(show_dialog)

    w.show()
    sys.exit(app.exec_())

def show_dialog():
    error_dialog = QDialog()
    error_dialog.setGeometry(100, 100, DIALOG_WIDTH, DIALOG_HEIGHT)
    error_dialog.exec_()

if __name__ == '__main__':
    window()
