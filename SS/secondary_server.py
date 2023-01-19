from datetime import datetime as dt
import time
import re
import os
import socket

now = str(dt.now())


class Secondary_server:
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
        self.db_info = ''
        self.db_domain = []
        self.db_all = {}

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

            if list[1] == 'SP':
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
        f.write(now + ' SS ' + self.ip + ' ' + str(self.port) +
                ' ' + str(self.ttl) + ' ' + self.mode + ' \n')
        f.write(now + ' EV @ conf-file-read ' + self.config_path + '\n')
        f.write(now + ' EV @ log-file-create ' + self.all_log_path + '\n')
        f.close()

        self.root_parser(self.root_path)
        for new_s, new_val in self.dns_all.items():
            for key, val in new_val.items():
                if key == 'DB':
                    self.db_parser(val)

        print(self.root_path)
        print(self.all_log_path)
        print(self.dns_all)

################################################################################################
# Zone transfer

    def remove_end_spaces(self, string):
        return "".join(string.rstrip())

    def zone_transfer(self, domain):

        server_info = self.dns_all.get(domain).get('SP')[0].split(':')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((server_info[0], int(server_info[1])))
            tcp_socket.send(domain.encode())
            print(tcp_socket.recv(1024).decode().replace('b', ''))
            accept = input()
            tcp_socket.send(accept.encode())

            self.db_info = tcp_socket.recv(1024).decode()
            db_domain_temp = self.db_info.split('z ')

            while ('' in db_domain_temp):
                db_domain_temp.remove('')

            for value in db_domain_temp:
                value = self.remove_end_spaces(value)
                self.db_domain.append(re.sub(r'^.*: ', '', value))

            self.db_all.update({domain: self.db_domain})
            print(self.db_all)


ss = Secondary_server('10.0.0.2', 86, 100, 'debug',
                      r'/home/core/DNS/dns/.ptgg/config/SS.config')

ss.config_parser()
ss.zone_transfer('new.ptgg.')
