import socket
import secondary_server as SS
import re
import threading


# Inicalize SR server

ss = SS.Secondary_server('127.0.0.1', 5353, 100, 'debug',
                         r'C:\Users\guiar\Documents\DNS\dns\.ptgg\config\config.ptgg\SS.ptgg.config')
ss.config_parser()

localIP = ss.ip
portUDP = ss.port
bufferSize = 1024

# Create a UDP socket at Resolve Server side

UDPss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip

UDPss.bind((localIP, portUDP))

# Create the logic for the sockets


def udp_listen(conn):
    while True:

        bytesAddressPair = conn.recvfrom(bufferSize)

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientIP)
        print(clientMsg)

        query = re.sub("b", "", clientMsg)
        query = re.sub("'", "", query)

        ss.pdu_temp_received = query.split(';')

        while '' in ss.pdu_temp_received:
            ss.pdu_temp_received.remove('')

        ss.pdu_received.clear()

        for line in ss.pdu_temp_received:
            temp2 = line.split(',')
            ss.pdu_received.append(temp2)

        print(ss.pdu_received)

        msgFromServer = str('Query received! Waiting to resolve...')

        bytesToSend = str.encode(msgFromServer)
        conn.sendto(bytesToSend, address)

# Create the listen threads


t1 = threading.Thread(target=udp_listen, args=(UDPss,))

print("Waiting for connections...")

t1.start()
t1.join()
