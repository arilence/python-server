"""---------------------------------------------------------------------------------------
--      SOURCE FILE:        Client.py - Client side connection methods
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
--      This file establishes a connection with a TCP server specified by the user. After
--      connected, the class will accept GET or SEND commands via methods. GET and SEND
--      require the filename to be passed. From there, the class will determine file sizes
--      and absolute locations to properly send or receive a file.
---------------------------------------------------------------------------------------"""
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

        self.sockObj.send("GET," + fileName)
        data = self.sockObj.recv(self.size).split(',')

        print data

        if (len(data) == 1) or (len(data) > 2):
            print 'File not found on server'
            return False

        theFile = open(fullPath, 'wb')
        fileSize = data[1]
        l = self.sockObj.recv(self.size)
        receivedSize = len(l)
        print 'Receiving...'
        while (l):
            #print 'Receiving... ' + str(receivedSize)
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
        #fileSize = os.path.getsize(fileLocation)
        fileSize = os.stat(fileLocation).st_size
        print fileSize

        self.sockObj.send("SEND," + tailName + "," + str(fileSize))
        theFile = open(fileLocation, 'rb')
        l = theFile.read(self.size)
        # wait for response before sending
        response = self.sockObj.recv(self.size)
        if (response == "OKAY"):
            print 'Sending...'
            while (l):
                self.sockObj.send(l)
                l = theFile.read(self.size)
            theFile.close()
            print 'Done Sending...'

            # Receive Server Response
            data = self.sockObj.recv(self.size)
            print data
            return True
        else:
            return False
