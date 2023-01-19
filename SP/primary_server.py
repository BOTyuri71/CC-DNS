from datetime import datetime as dt
import time
import re
import os

now = str(dt.now())


class Primary_server:
    def __init__(self, ip, port, ttl, mode, config_path):
        self.ip = str(ip)
        self.port = int(port)
        self.ttl = int(ttl)
        self.mode = str(mode)
        self.config_path = str(config_path)

#############################################################################################

# Config info

        self.config_read = []
        self.config_parsed = []

        self.all_log_path = ''
        self.root_path = ''
        self.dns_all = {}

#############################################################################################

# Root info

        self.root_read = []
        self.root_parsed = []

        self.root_all = {}

#############################################################################################

# Data info

        self.db_read = []
        self.db_parsed = []

        self.default = ''
        self.db_ns = {}
        self.db_mx = {}
        self.db_www = {}
        self.db_ftp = {}
        self.db_all = {}
        self.db_domain = {}

#############################################################################################

# Pdu received info

        self.pdu_temp_received = []
        self.pdu_received = []

#############################################################################################

# Pdu to send info

        self.pdu_temp_send = []
        self.pdu_send = []

##############################################################################################

# Zone transfer

        self.entries = 0
        self.db_zones = {}
        self.db_zone = []

##############################################################################################

# Root Parser

    def root_parser(self, path):
        with open(path) as f:
            config = f.readlines()

        for line in config:
            self.root_read.append(line.replace('\n', ''))

        for line in self.root_read:
            if (line.startswith('#')):
                self.root_read.remove(line)
            if (line.startswith(' ')):
                self.root_read.remove(line)

        while ("" in self.root_read):
            self.root_read.remove("")

        for line in self.root_read:
            temp = line.split(' ')

            for i in temp:
                if i == '':
                    temp.remove(i)
                if i == 'ST':
                    temp.remove(i)

            self.root_parsed.append(temp)

        for list in self.root_parsed:

            for i in list:
                temp = i.split(':')
                self.root_all.update({temp[0]: int(temp[1])})

##############################################################################################

# DB Parser

    def db_parser(self, path):

        with open(path) as f:
            config = f.readlines()

        for line in config:
            self.db_read.append(line.replace('\n', ''))

        for line in self.db_read:
            if (line.startswith('#')):
                self.db_read.remove(line)
            if (line.startswith(' ')):
                self.db_read.remove(line)

        while ("" in self.db_read):
            self.db_read.remove("")

        for line in self.db_read:
            temp = line.split(' ')

            for i in temp:
                if i == '':
                    temp.remove(i)

            self.db_parsed.append(temp)

        for list in self.db_parsed:
            if list[0] == '@' and list[1] == 'DEFAULT':
                self.default = list[2]
            if list[0] == 'TTL' and list[1] == 'DEFAULT':
                self.db_domain.update({list[0]: int(list[2])})
            if list[0] == '@' and list[1] == 'SOAADMIN':
                temp1 = list[2]
                soa_admin = re.sub("\\\.", ".", temp1)
                self.db_domain.update({list[1]: soa_admin})
            if list[0] == '@' and list[1] == 'SOASERIAL':
                self.db_domain.update({list[1]: int(list[2])})
            if list[0] == '@' and list[1] == 'SOAREFRESH':
                self.db_domain.update({list[1]: int(list[2])})
            if list[0] == '@' and list[1] == 'SOARETRY':
                self.db_domain.update({list[1]: int(list[2])})
            if list[0] == '@' and list[1] == 'SOAEXPIRE':
                self.db_domain.update({list[1]: int(list[2])})
            if list[1] == 'NS' and 4 < len(list):
                if list[1] not in self.db_domain:
                    self.db_domain.update({list[1]: {}})
                self.db_domain[list[1]].update({list[2]: int(list[4])})
            elif list[1] == 'NS':
                if list[1] not in self.db_domain:
                    self.db_domain.update({list[1]: {}})
                self.db_domain[list[1]].update({list[2]: 0})
            if list[1] == 'MX' and 4 < len(list):
                if list[1] not in self.db_domain:
                    self.db_domain.update({list[1]: {}})
                self.db_domain[list[1]].update({list[2]: int(list[4])})
            elif list[1] == 'MX':
                if list[1] not in self.db_domain:
                    self.db_domain.update({list[1]: {}})
                self.db_domain[list[1]].update({list[2]: 0})
            if list[1] == 'A' and 4 < len(list):
                if list[0] not in self.db_domain:
                    if 'NS' in self.db_domain:
                        for value in self.db_domain['NS']:
                            if list[0] in value:
                                self.db_domain['NS'].update(
                                    {value + list[1] + list[2]: int(list[4])})
                    if 'MX' in self.db_domain:
                        for value in self.db_domain['MX']:
                            if list[0] in value:
                                self.db_mx.update(
                                    {value + ' ' + list[1] + ' ' + list[2]: 0})
                    if list[0] == 'www':
                        self.db_www.update(
                            {list[0] + ' ' + list[1] + ' ' + list[2]: int(list[4])})
                    if list[0] == 'ftp':
                        self.db_ftp.update(
                            {list[0] + ' ' + list[1] + ' ' + list[2]: int(list[4])})
            elif list[1] == 'A':
                if list[0] not in self.db_domain:
                    if 'NS' in self.db_domain:
                        for value in self.db_domain['NS']:
                            if list[0] in value:
                                self.db_ns.update(
                                    {value + ' ' + list[1] + ' ' + list[2]: 0})
                    if 'MX' in self.db_domain:
                        for value in self.db_domain['MX']:
                            if list[0] in value:
                                self.db_mx.update(
                                    {value + ' ' + list[1] + ' ' + list[2]: 0})
                    if list[0] == 'www':
                        self.db_www.update(
                            {list[0] + ' ' + list[1] + ' ' + list[2]: 0})
                    if list[0] == 'ftp':
                        self.db_ftp.update(
                            {list[0] + ' ' + list[1] + ' ' + list[2]: 0})
            if list[1] == 'CNAME':
                if list[1] not in self.db_domain:
                    self.db_domain.update({list[1]: {}})
                self.db_domain[list[1]].update({list[0]: list[2]})

        self.db_zones.update({self.default: self.db_read})
        if self.db_ns != {}:
            self.db_domain['NS'] = self.db_ns
        if self.db_mx != {}:
            self.db_domain['MX'] = self.db_mx
        if self.db_www != {}:
            self.db_domain.update({'www': self.db_www})
        if self.db_ftp != {}:
            self.db_domain.update({'ftp': self.db_ftp})
        self.db_all.update({self.default: self.db_domain})

        # print(self.db_all)

        f = open(self.all_log_path, "a")
        f.write(now + ' EV @ db-file-read ' + path + '\n')
        f.close()


################################################################################################
# Config parser

    def config_parser(self):

        with open(self.config_path) as f:
            config = f.readlines()

        for line in config:
            self.config_read.append(line.replace('\n', ''))

        for line in self.config_read:
            if (line.startswith('#')):
                self.config_read.remove(line)
            if (line.startswith(' ')):
                self.config_read.remove(line)

        while ("" in self.config_read):
            self.config_read.remove("")

        for line in self.config_read:
            temp = line.split(' ')

            for i in temp:
                if i == '':
                    temp.remove(i)

            self.config_parsed.append(temp)

        for list in self.config_parsed:

            if list[0] not in self.dns_all and (list[0] != 'all') and (list[0] != 'root'):
                self.dns_all[list[0]] = {}

            if list[1] == 'DB':
                self.dns_all[list[0]].update({list[1]: list[2]})

            if list[1] == 'SS':
                if list[1] not in self.dns_all[list[0]]:
                    self.dns_all[list[0]].update({list[1]: []})
                self.dns_all[list[0]][list[1]].append(list[2])

            if list[1] == 'DD':
                self.dns_all[list[0]].update({list[1]: list[2]})

            if list[0] == 'all' and list[1] == 'LG':
                self.all_log_path = list[2]
            elif list[1] == 'LG':
                self.dns_all[list[0]].update({list[1]: list[2]})

            if list[0] == 'root' and list[1] == 'ST':
                self.root_path = list[2]

        f = open(self.all_log_path, "a")
        f.write(now + ' SP ' + self.ip + ' ' + str(self.port) +
                ' ' + str(self.ttl) + ' ' + self.mode + ' \n')
        f.write(now + ' EV @ conf-file-read ' + self.config_path + '\n')
        f.write(now + ' EV @ log-file-create ' + self.all_log_path + '\n')
        f.close()

        self.root_parser(self.root_path)
        for new_s, new_val in self.dns_all.items():
            for key, val in new_val.items():
                if key == 'DB':
                    self.db_parser(val)


################################################################################################
# Pdu to send

    def pdu_build(self):
        self.pdu_send = self.pdu_received

        print(self.pdu_received[1][0])
        print(self.db_all.keys())

        if (self.pdu_received[1][0] in self.db_all.keys()):
            print('blaa')

################################################################################################
# Zone transfer

    def zone_transfer(self, domain):

        if domain in self.db_zones:
            self.db_zone = self.db_zones.get(domain)

            self.db_zone[0] = self.db_zone[0].replace('@', '')
            self.db_zone[0] = self.db_zone[0].replace('DEFAULT', '')
            self.db_zone[0] = self.db_zone[0].replace(' ', '')

            self.db_zone[1] = self.db_zone[1].replace('TTL', '')
            self.db_zone[1] = self.db_zone[1].replace('DEFAULT', '')
            self.db_zone[1] = self.db_zone[1].replace(' ', '')

            dns_temp = self.db_zone[0] + ' '
            dns_temp2 = self.db_zone[1]

            self.db_zone = [sub.replace('@ ', dns_temp)
                            for sub in self.db_zone]
            self.db_zone = [sub.replace('TTL', dns_temp2)
                            for sub in self.db_zone]

            del self.db_zone[0]
            del self.db_zone[0]

            for value in self.db_zone:
                self.entries = self.entries+1

        else:
            print("Este servidor primário não tem informação sobre o domínio pedido!")

################################################################################################
# Pdu response

    def query_response(self, domain, serverAddressPort, socket):
        for key in self.db_all:
            if key in domain:
                self.pdu_send = str(key) + ':' + str(self.db_all[key])

                bytesToSend = str.encode(self.pdu_send)
                socket.sendto(bytesToSend, serverAddressPort)
