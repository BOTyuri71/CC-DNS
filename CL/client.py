import socket
import argparse

ip_destino = ''
name = ''
type_of_value = ''
recursive_mode = False


###################################################################

# Terminal Parser

def terminal_parser(input):

    data = input.split(' ')

    if data[0] == 'dnscl' and len(data) > 3:
        ip_destino = data[1]
        name = data[2]
        type_of_value = data[3]

        if (len(data) > 4):
            if (data[4] == 'R'):
                recursive_mode = True
    else:
        print('Formato incorreto')

    print(ip_destino)
    print(name)
    print(type_of_value)

#################################################################


terminal = str(input())
terminal_parser(terminal)

msgFromClient = "Hello UDP Server"

bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("127.0.0.1", 59)

bufferSize = 1024


# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)


msgFromServer = UDPClientSocket.recvfrom(bufferSize)

another_str = str(msgFromServer)
another_str = another_str.replace('\\\\\\', '\\')
another_str = another_str.replace('b"', '')
