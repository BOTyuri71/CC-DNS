import socket
import client as cl

cl = cl.Client()
terminal = str(input())
cl.terminal_parser(terminal)

msgFromClient = str(cl.pdu_to_string())

bytesToSend = str.encode(msgFromClient)

localIP = '10.1.1.1'
localPort = 53
bufferSize = 1024


# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, localPort)


msgFromServer = UDPClientSocket.recvfrom(bufferSize)


msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
