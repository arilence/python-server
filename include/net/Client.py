from socket import *
import ntpath, os, sys

class Client:
    def __init__(self, host, port):
        # Initialize Vars and Socket
        self.remoteHost = host
        self.remotePort = port
        self.size = 1024
        self.directory = 'client'
        self.sockObj = socket(AF_INET, SOCK_STREAM)

        # Connect To Remote
        self.sockObj.connect((self.remoteHost, self.remotePort))

    def get(self, fileName):
        # Make sure file folder exists
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        fileLoc = os.path.join(self.directory, fileName)
        tailName = ntpath.basename(fileLoc)
        fullPath = os.path.abspath(fileLoc)

        self.sockObj.send("GET " + fileName)
        data = self.sockObj.recv(self.size).split(',')

        print data

        if (len(data) == 1) or (len(data) > 2):
            print 'File not found on server'
            return False

        theFile = open(fullPath, 'wb')
        fileSize = data[1]
        l = self.sockObj.recv(self.size)
        receivedSize = len(l)
        while (l):
            print 'Receiving... ' + str(receivedSize)
            theFile.write(l)

            if (str(receivedSize) != fileSize):
                l = self.sockObj.recv(self.size)
                receivedSize = receivedSize + len(l)
            else:
                break
        theFile.close()
        print 'Done Receiving'
        return True

    def send(self, fileLocation):
        tailName = ntpath.basename(fileLocation)
        fileSize = os.path.getsize(fileLocation)

        self.sockObj.send("SEND," + tailName + "," + str(fileSize))
        theFile = open(fileLocation, 'rb')
        l = theFile.read(self.size)
        while (l):
            print 'Sending...'
            self.sockObj.send(l)
            l = theFile.read(self.size)
        theFile.close()
        print 'Done Sending...'

        # Receive Server Response
        data = self.sockObj.recv(self.size)
        print data
        return True
