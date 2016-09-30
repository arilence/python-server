from socket import *
from threading import *
import ntpath
import os
import sys

class Server:
    def __init__(self):
        # Initialize Variables and Socket
        self.listenHost = ''
        self.listenPort = 7005
        self.size = 1024
        self.sockObj = socket(AF_INET, SOCK_STREAM)
        self.sockObj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # Bind Socket
        try:
            self.sockObj.bind((self.listenHost, self.listenPort))
            self.sockObj.listen(5)
        except:
            self.print_error_message('Socket couldn\'t be binded')
            raise

        # Wait for Connection
        while True:
            client, address = self.sockObj.accept()
            self.print_info_message('Client Connection: ' + str(address))
            Thread(target = self.listenToClient, args = (client, address)).start()

    def listenToClient(self, client, address):
        default_file_location = 'server'

        while True:
            try:
                data = (client.recv(self.size)).split()

                if data:
                    if (data[0] == "GET"):
                        tailName = ntpath.basename(data[1])
                        fullPath = os.path.abspath(data[1])
                        fileSize = os.path.getsize(data[1])
                        print tailName

                        client.send(tailName + " " + str(fileSize))
                        theFile = open(fullPath, 'rb')
                        l = theFile.read(self.size)
                        while(l):
                            self.print_info_message('Sending...')
                            client.send(l)
                            l = theFile.read(self.size)
                        theFile.close()
                        self.print_info_message('Done Sending')

                    if (data[0] == "SEND"):
                        self.print_info_message('Saving to ' + str(data[1]))
                        self.print_info_message('File size: ' + str(data[2]) + ' bytes')

                        theFile = open(data[1], 'wb')
                        fileSize = data[2]
                        l = client.recv(self.size)
                        receivedSize = len(l)       # keep track of transferred bytes
                        while (l):
                            self.print_info_message("Receiving... " + str(receivedSize))
                            theFile.write(l)

                            if (str(receivedSize) != fileSize): # know when to stop receiving data
                                l = client.recv(self.size)
                                receivedSize = receivedSize + len(l)
                            else:
                                break
                        theFile.close()
                        self.print_info_message('Done Receiving')
                        client.send("File Received Successfully")
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

    def print_error_message(self, text):
        print('ERROR: ' + text)

    def print_info_message(self, text):
        print('INFO: ' + text)

if __name__ == "__main__":
    try:
        server = Server()
    except KeyboardInterrupt:
        print('\nClosing... Have a nice day :)')
        sys.exit()
