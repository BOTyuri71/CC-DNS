from datetime import datetime as dt
import time
import re
import os

now = str(dt.now())


class dns_resolver:
    def __init__(self, ip, port, ttl, mode, config_path):
        self.ip = str(ip)
        self.port = int(port)
        self.ttl = int(ttl)
        self.mode = str(mode)
        self.config_path = str(config_path)

#############################################################################################

# Config variables

        self.config_read = []
        self.config_parsed = []
        self.dd_ip = ''
        self.all_log_path = ''
        self.root_path = ''
        self.dns_all = {}

#############################################################################################

# Root variables

        self.root_read = []
        self.root_parsed = []
        self.root_all = {}

#############################################################################################

# Data variables

        self.db_read = []
        self.db_parsed = []
        self.default = ''
        self.db_domain = {}
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
                self.default_ip = list[2]

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
