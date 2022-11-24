import socket
import argparse
import struct
import random


class Client:

    ###################################################################
    # Input variables

    ip_destino = ''
    name = ''
    type_of_value = ''
    recursive_mode = False

    ###################################################################
    # DNS message variables

    pdu = []
    header = {}
    data = {}
    query_info_fields = {}

    ###################################################################

    # Terminal Parser

    def terminal_parser(self, input):

        data = input.split(' ')

        if data[0] == 'dnscl' and len(data) > 3:
            self.ip_destino = data[1]
            self.name = data[2]
            self.type_of_value = data[3]

            if (len(data) > 4):
                if (data[4] == 'R'):
                    self.recursive_mode = True
        else:
            print('Formato incorreto')

#################################################################

    def header_builder(self):
        self.header.update({'MESSAGE_ID': random.randint(1, 65535)})
        if self.recursive_mode == True:
            self.header.update({'FLAGS': 'Q+R'})
        elif self.recursive_mode == False:
            self.header.update({'FLAGS': 'Q'})
        self.header.update({'RESPONSE-CODE': 0})
        self.header.update({'N-VALUES': 0})
        self.header.update({'N-AUTHORITIES': 0})
        self.header.update({'N-EXTRA-VALUES': 0})

    def query_info_builder(self):
        self.query_info_fields.update({'NAME': self.name})
        self.query_info_fields.update({'TYPE OF VALUE': self.type_of_value})

    def data_builder(self):
        self.query_info_builder()
        self.data.update({'RESPONSE VALUES': {}})
        self.data.update({'AUTHORITIES VALUES': {}})
        self.data.update({'EXTRA VALUES': {}})

    def pdu_builder(self):
        self.header_builder()
        self.data_builder()

        self.pdu.append(self.header)
        self.pdu.append(self.data)
        print(self.pdu)


cl = Client()
terminal = str(input())
cl.terminal_parser(terminal)
cl.pdu_builder()
