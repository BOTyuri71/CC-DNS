import socket
import argparse
import struct
import random


class Client:

    ###################################################################
    # Input variables

    ip_destino = []
    name = ''
    type_of_value = ''
    recursive_mode = False

    ###################################################################
    # DNS query variables

    query_pdu = []
    query_header = {}
    query_data = {}
    query_info_fields = {}

    qheader_str = ''
    qdata_str = ''
    qpdu_str = ''

    ###################################################################
    # DNS response variables

    response_pdu = []
    response_header = {}
    response_data = {}
    response_info_fields = {}

    rheader_str = ''
    rdata_str = ''
    rpdu_str = ''

    ###################################################################

    # Terminal Parser

    def terminal_parser(self, input):

        data = input.split(' ')

        if data[0] == 'dnscl' and len(data) > 3:
            temp_ip = data[1].split(':')
            self.ip_destino = temp_ip
            self.name = data[2]
            self.type_of_value = data[3]

            if (len(data) > 4):
                if (data[4] == 'R'):
                    self.recursive_mode = True
        else:
            print('Formato incorreto')

    #################################################################

    def header_builder(self):
        self.query_header.update({'MESSAGE_ID': random.randint(1, 65535)})
        if self.recursive_mode == True:
            self.query_header.update({'FLAGS': 'Q+R'})
        elif self.recursive_mode == False:
            self.query_header.update({'FLAGS': 'Q'})
        self.query_header.update({'RESPONSE-CODE': 0})
        self.query_header.update({'N-VALUES': 0})
        self.query_header.update({'N-AUTHORITIES': 0})
        self.query_header.update({'N-EXTRA-VALUES': 0})

    def query_info_builder(self):
        self.query_info_fields.update({'NAME': self.name})
        self.query_info_fields.update({'TYPE OF VALUE': self.type_of_value})

    def data_builder(self):
        self.query_info_builder()
        self.query_data.update({'RESPONSE VALUES': {}})
        self.query_data.update({'AUTHORITIES VALUES': {}})
        self.query_data.update({'EXTRA VALUES': {}})

    def pdu_builder(self):
        self.header_builder()
        self.data_builder()

    #################################################################

    def pdu_to_string(self):

        self.pdu_builder()

        self.qheader_str = str(self.query_header['MESSAGE_ID']) + ',' + self.query_header['FLAGS'] + ',' + str(self.query_header['RESPONSE-CODE']) + \
            ',' + str(self.query_header['N-VALUES']) + ',' + \
            str(self.query_header['N-AUTHORITIES']) + ',' + \
            str(self.query_header['N-EXTRA-VALUES'])

        self.qdata_str = str(
            self.query_info_fields['NAME'] + ',' + self.query_info_fields['TYPE OF VALUE'])

        self.qpdu_str = self.qheader_str + ';' + self.qdata_str + ';'
