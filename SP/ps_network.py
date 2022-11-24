import socket
import primary_server as ps

localIP = "127.0.0.1"
localPort = 59
bufferSize = 1024

sp = ps.primary_server('10.0.0.2', 86, 100, 'debug',
                       r'C:\Users\guiar\dns\.ptgg\config\SP.config')

sp.config_parser()

msgFromServer = str(sp.dns_all)

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
    print(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
