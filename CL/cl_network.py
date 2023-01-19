import socket
import client as cl
import re

cl = cl.Client()
bufferSize = 1024

while True:
    terminal = str(input())
    cl.terminal_parser(terminal)
    cl.pdu_to_string()

    localIP = str(cl.ip_destino[0])
    localPort = int(cl.ip_destino[1])
    serverAddressPort = (localIP, localPort)

    msgFromClient = cl.qpdu_str

    bytesToSend = str.encode(msgFromClient)


# Create a UDP socket at client side

    UDPClientSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    response = "{}".format(msgFromServer[0])
    msg = re.sub("b", "", response)
    msg = re.sub("'", "", msg)

    print(msg + '\n')
