from datetime import datetime as dt
import time
import re
import os

now = str(dt.now())


class Resolve_server:
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

# Cache info

        self.cache_domain = {}
        self.cache_all = {}


#############################################################################################

# Pdu received info

        self.pdu_temp_received = []
        self.pdu_received = []


##############################################################################################

# Root Parser

    def root_parser(self, path):
        with open(path) as f:
            config = f.readlines()

        for line in config:
            self.root_read.append(line.replace('\n', ''))

        print(self.root_read)

        for line in self.root_read:
            if (line.startswith('#')):
                self.root_read.remove(line)
            if (line.startswith(' ')):
                self.root_read.remove(line)

        print(self.root_read)

        while ("" in self.root_read):
            self.root_read.remove("")

        print(self.root_read)

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
        f.write(now + ' SR ' + self.ip + ' ' + str(self.port) +
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
        print(self.root_all)

################################################################################################
# Query resolver

    def query_resolver_top(self, msg, query, socket):
        if len(query) > 1:
            if query[1][0] in self.cache_all:
                query_response = self.cache_all.get(query[1][0])
            else:
                for key in self.root_all:
                    try:
                        msgFromClient = re.sub("b", "", msg)
                        msgFromClient = re.sub("'", "", msgFromClient)

                        serverAddressPort = (key, self.root_all[key])
                        bytesToSend = str.encode(msgFromClient)
                        socket.sendto(bytesToSend, serverAddressPort)
                    except:
                        pass
