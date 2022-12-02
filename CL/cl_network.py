import socket
import client as cl

cl = cl.Client()
terminal = str(input())
cl.terminal_parser(terminal)

msgFromServer = str(cl.pdu_to_string())

bytesToSend = str.encode(msgFromServer)

localIP = cl.ip_destino[0]
localPort = cl.ip_destino[1]
bufferSize = 1024

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
    print(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
