from socket import *
import ntpath, os, sys, argparse

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

    def start(self):
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
            if (command.upper() == "GET"):
                # Make sure file folder exists
                if not os.path.exists(self.directory):
                    os.makedirs(self.directory)

                fileLoc = os.path.join(self.directory, fileName)
                tailName = ntpath.basename(fileLoc)
                fullPath = os.path.abspath(fileLoc)

                self.sockObj.send(command + " " + fileName)
                data = self.sockObj.recv(self.size).split()

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


            elif (command.upper() == "SEND"):
                tailName = ntpath.basename(fileName)
                fullPath = os.path.abspath(fileName)
                fileSize = os.path.getsize(fileName)

                self.sockObj.send(command + " " + tailName + " " + str(fileSize))
                theFile = open(fullPath, 'rb')
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

def parseCmdArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='host ip to bind to', default='localhost')
    parser.add_argument('--port', help='port number to listen on', default=7005, type=int)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Parse Input Arguments
    args = parseCmdArguments()

    try:
        client = Client(args.ip, args.port)
        client.start()
    except KeyboardInterrupt:
        print('\nClosing... Have a nice day :)')
        sys.exit()
