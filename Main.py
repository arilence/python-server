import sys, argparse
from socket import gethostbyname, gaierror
from PyQt4 import QtGui
from PyQt4.QtGui import *
from include.gui.ConnectionDialog import ConnectionDialog
from include.gui.GetDialog import GetDialog
from include.gui.SendDialog import SendDialog
from include.gui.ErrorDialog import ErrorDialog
from include.gui.MessageDialog import MessageDialog
from include.net.Client import Client
from include.net.Server import Server

class ClientApplication:
    def __init__(self, remoteHost, remotePort):
        self.app = QtGui.QApplication(sys.argv)
        connectionDialog = ConnectionDialog(remoteHost, remotePort)
        if (connectionDialog.exec_()):
            try:
                client = Client(str(connectionDialog.remoteHost), remotePort)
                window = MainWindow(client)
                window.show()
            except gaierror:
                ErrorDialog("Cannot connect to host").exec_()
                raise
        else:
            sys.exit()

        sys.exit(self.app.exec_())

class MainWindow(QWidget):
    WINDOW_HEIGHT = 150
    WINDOW_WIDTH = 500

    def __init__(self, client, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.client = client
        self.setGeometry(100, 100, MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
        self.setWindowTitle("File Transfer App")
        self.center()

        b = QPushButton(self)
        b.setText("GET")
        b.setFixedHeight(50)
        b.clicked.connect(self.get_dialog)

        b2 = QPushButton(self)
        b2.setText("SEND")
        b2.setFixedHeight(50)
        b2.clicked.connect(self.send_dialog)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(b)
        grid.addWidget(b2)
        self.setLayout(grid)

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def get_dialog(self):
        getDialog = GetDialog()
        if (getDialog.exec_()):
            fileName = str(getDialog.fileName)
            if (len(fileName) <= 0) or (len(fileName) > 256):
                ErrorDialog("File name must be between 3 and 256 characters").exec_()
            else:
                if (self.client.get(str(getDialog.fileName))):
                    MessageDialog("File was downloaded successfully").exec_()
                else:
                    ErrorDialog("File was not found on the server").exec_()

    def send_dialog(self):
        sendDialog = SendDialog()
        if (sendDialog.exec_()):
            fileLocation = str(sendDialog.fileLocation)
            if (len(fileLocation) <= 0):
                ErrorDialog("File location cannot be empty").exec_()
            else:
                if (self.client.send(str(sendDialog.fileLocation))):
                    MessageDialog("File was uploaded successfully").exec_()
                else:
                    ErrorDialog("Hmm... there was a problem uploading the file").exec_()

def parseCmdArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='host ip to bind to', default='localhost')
    parser.add_argument('--port', help='port number to listen on', default=7005, type=int)
    parser.add_argument('--server', help='starts up in server mode', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Parse Input Arguments
    args = parseCmdArguments()

    if (args.server):
        try:
            server = Server(args.ip, args.port)
        except KeyboardInterrupt:
            print('\nClosing... Have a nice day :)')
            sys.exit()
    else:
        ClientApplication(args.ip, args.port)
