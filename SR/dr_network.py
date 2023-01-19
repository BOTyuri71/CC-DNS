import socket
import dns_resolver as RS
import re
import threading
import json


# Inicalize SR server

rs = RS.Resolve_server('127.0.0.1', 1035, 100, 'debug',
                       r'C:\Users\guiar\Documents\DNS\dns\.ptgg\config\SR.config')
rs.config_parser()

localIP = rs.ip
portUDP = rs.port
bufferSize = 1024

# Create a UDP socket at Resolve Server side

UDPrs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip

UDPrs.bind((localIP, portUDP))

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

        rs.pdu_temp_received = query.split(';')

        while '' in rs.pdu_temp_received:
            rs.pdu_temp_received.remove('')

        rs.pdu_received.clear()

        for line in rs.pdu_temp_received:
            temp2 = line.split(',')
            rs.pdu_received.append(temp2)

        msgFromServer = str('Query received! Waiting to resolve...')
        bytesToSend = str.encode(msgFromServer)
        conn.sendto(bytesToSend, address)

        rs.query_resolver_top(clientMsg, rs.pdu_received, conn)

        clientMsg = "{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        msgFromClient = re.sub("b", "", clientMsg)
        msgFromClient = re.sub(r'^"', "", msgFromClient)
        msgFromClient = re.sub(r'"$', "", msgFromClient)
        print(msgFromClient)
        if len(re.findall(r'^[a-z.]', msgFromClient)) > 0:
            if (re.findall(r'^[^:]*', msgFromClient)):
                key = str(re.findall(r'^[^:]*', msgFromClient)[0])
            msgFromClient = re.sub(r'^[^:]*', "", msgFromClient)
            value = re.sub(r'^:', "", msgFromClient)

            rs.cache_domain.update({key: value})
            print(rs.cache_domain)


# Create the listen threads
t1 = threading.Thread(target=udp_listen, args=(UDPrs,))

print("Waiting for connections...")

t1.start()
t1.join()
