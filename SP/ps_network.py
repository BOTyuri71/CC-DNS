import socket
import primary_server as ps
import re

localIP = "10.2.2.2"
localPort = 53
bufferSize = 1024

sp = ps.Primary_server('10.2.2.2', 86, 100, 'debug',
                    r'/home/core/DNS/dns/.ptgg/config/SP.config')

sp.config_parser()

msgFromServer = str('hello')

bytesToSend = str.encode(msgFromServer)


# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))


print("UDP server up and listening")


# Listen for incoming datagrams

while (True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client: {}".format(message)

    clientIP = "Client IP Address:{}".format(address)

    msg = re.sub("b", "", clientMsg)

    print(msg)

    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
