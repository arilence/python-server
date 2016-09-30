from socket import *
import ntpath
import os

if __name__ == "__main__":
    # Initialize Vars and Socket
    remoteHost = 'localhost'
    remotePort = 7005
    sockObj = socket(AF_INET, SOCK_STREAM)

    # Connect To Remote
    sockObj.connect((remoteHost, remotePort))

    while True:
        # Wait for User Input
        userInput = raw_input("Enter a command: ")
        splitInput = userInput.split()
        if (len(splitInput) != 2):
            print 'Please enter 2 arguments'
            continue
        command = splitInput[0]
        fileName = splitInput[1]

        # Check Command
        if (command == "GET"):
            sockObj.send(command + " " + fileName)
            data = sockObj.recv(1024).split()
            print data

            theFile = open('test.txt', 'wb')
            fileSize = data[1]
            l = sockObj.recv(1024)
            receivedSize = len(l)
            while (l):
                print 'Receiving... ' + str(receivedSize)
                theFile.write(l)

                if (str(receivedSize) != fileSize):
                    l = sockObj.recv(1024)
                    receivedSize = receivedSize + len(l)
                else:
                    break
            theFile.close()
            print 'Done Receiving'


        elif (command == "SEND"):
            tailName = ntpath.basename(fileName)
            fullPath = os.path.abspath(fileName)
            fileSize = os.path.getsize(fileName)
            print fullPath

            sockObj.send(command + " " + tailName + " " + str(fileSize))
            theFile = open(fullPath, 'rb')
            l = theFile.read(1024)
            while (l):
                print 'Sending...'
                sockObj.send(l)
                l = theFile.read(1024)
            theFile.close()
            print 'Done Sending...'

            # Receive Server Response
            data = sockObj.recv(1024)
            print data
