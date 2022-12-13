import socket
import client as cl

cl = cl.Client()
terminal = str(input())
cl.terminal_parser(terminal)
cl.pdu_to_string()

msgFromClient = cl.qpdu_str

bytesToSend = str.encode(msgFromClient)

localIP = '10.2.2.2'
localPort = 53
bufferSize = 1024

serverAddressPort = (localIP, localPort)


# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)


msgFromServer = UDPClientSocket.recvfrom(bufferSize)


msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
