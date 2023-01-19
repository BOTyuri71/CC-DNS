import socket
import primary_server as PS
import re
import threading

# Inicalize SP server

sp = PS.Primary_server('127.0.0.1', 53, 100, 'debug',
                       r'C:\Users\guiar\Documents\DNS\dns\.ptgg\config\SP.config')
sp.config_parser()

localIP = sp.ip
portUDP = sp.port
portTCP = 65432
bufferSize = 1024


# Create a datagram socket

sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to address and ip

sockUDP.bind((localIP, portUDP))
sockTCP.bind((localIP, portTCP))
sockTCP.listen(20)

# Create the logic for the sockets


def udp_listen(conn):
    while True:

        bytesAddressPair = conn.recvfrom(bufferSize)

        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        print(clientMsg)

        query = re.sub("b", "", clientMsg)
        query = re.sub("'", "", query)

        sp.pdu_temp_received = query.split(';')

        while '' in sp.pdu_temp_received:
            sp.pdu_temp_received.remove('')

        sp.pdu_received.clear()

        for line in sp.pdu_temp_received:
            temp2 = line.split(',')
            sp.pdu_received.append(temp2)

        print(sp.pdu_received)

        if (len(sp.pdu_received) > 1):
            sp.query_response(sp.pdu_received[1][0], address, conn)


def tcp_listen(sock):
    conn, addr = sock.accept()
    print(f"Connected to Secondary Server {addr}")
    try:
        while True:
            data = conn.recv(1024)
            domain = data.decode().replace('b', '')
            print("domain: " + domain)

            sp.zone_transfer(domain)
            entries_to_send = "entries: " + str(sp.entries)
            conn.sendall(entries_to_send.encode())
            accept = conn.recv(1024).decode().replace('b', '')

            if (accept == 'yes'):
                counter = 1
                for value in sp.db_zone:
                    to_send = 'z ' + str(counter) + '/' + \
                        str(sp.entries) + ': ' + str(value)
                    conn.sendall(to_send.encode())
                    counter = counter+1

            break
            if len(data) == 0:
                break
            print("recv:", data)
    except Exception:
        pass
    try:
        conn.close()
        print(f"Connection closed to Secondary Server {addr}")
    except Exception:
        pass


# Create the listen threads
t1 = threading.Thread(target=tcp_listen, args=(sockTCP,))
t2 = threading.Thread(target=udp_listen, args=(sockUDP,))

print("Waiting for connections...")

t1.start()
t2.start()

t1.join()
t2.join()
