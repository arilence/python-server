"""---------------------------------------------------------------------------------------
--      SOURCE FILE:        Server.py - Server side connection methods
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
--      This file creates a TCP server with a specified port number. After binding to a
--      socket, the class waits for an incoming connection. Once a connection has been
--      been made, they are split off onto seperate threads for better performance.
--      Within each thread, the program waits for incoming commands (GET / SEND).
--      Depending on the command, the server will either read from or write to a file.
---------------------------------------------------------------------------------------"""
from socket import *
from threading import *
import ntpath, os, os.path, sys, argparse

class Server:
    def __init__(self, host, port):
        # Initialize Variables and Socket
        self.listenHost = host
        self.listenPort = port
        self.size = 1024
        self.directory = 'server'
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

        while True:
            try:
                data = (client.recv(self.size)).split(',')

                fileLoc = os.path.join(self.directory, data[1])

                if data:
                    if (data[0].upper() == "GET"):
                        if not (os.path.exists(fileLoc)):
                            self.print_error_message('file not found')
                            client.send('invalid')
                            continue

                        tailName = ntpath.basename(fileLoc)
                        fullPath = os.path.abspath(fileLoc)
                        fileSize = os.path.getsize(fileLoc)
                        self.print_info_message('Requested file: ' + tailName)

                        client.send(tailName + "," + str(fileSize))
                        theFile = open(fullPath, 'rb')
                        l = theFile.read(self.size)
                        while(l):
                            self.print_info_message('Sending...')
                            client.send(l)
                            l = theFile.read(self.size)
                        theFile.close()
                        self.print_info_message('Done Sending')


                    elif (data[0].upper() == "SEND"):
                        self.print_info_message('Saving to ' + str(data[1]))
                        self.print_info_message('File size: ' + str(data[2]) + ' bytes')

                        tailName = ntpath.basename(fileLoc)
                        fullPath = os.path.abspath(fileLoc)

                        # Make sure file folder exists
                        if not os.path.exists(self.directory):
                            os.makedirs(self.directory)

                        # Send response that file is received
                        client.send("OKAY")

                        theFile = open(fullPath, 'wb')
                        fileSize = data[2]
                        l = client.recv(self.size)
                        receivedSize = len(l)       # keep track of transferred bytes
                        while (l):
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
