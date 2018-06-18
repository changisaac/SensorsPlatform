# Name: Isaac Chang
# Date: June 17, 2018

import os
import sys
import socket
import json
import time

class SensorSubscriber:

    def __init__(self, channel_name, log=False, log_file=None):

        # sensor configs
        self.master_port = 8001
        self.max_recv_bytes = 1024
        self.log = log
        self.log_file = log_file
        self.file = None

        if log:
            self.log_file = "logs" + channel_name + "/logs.txt"
            dirname = os.path.dirname(self.log_file)
            
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            self.file = open(self.log_file, 'a+', 0)
            
        # setup subscriber sockets
        self.sensor_soc = socket.socket()
        self.host = socket.gethostname()

        try:
            self.sensor_soc.connect((self.host, self.master_port))
        except socket.error:
            return

        self.sensor_soc.settimeout(3)

        self.request_package = {"channel_name": channel_name}

    def request_data(self):
       
        try:
            self.sensor_soc.send(json.dumps(self.request_package))
            recv_data = self.sensor_soc.recv(self.max_recv_bytes)
            print("received on channel " + self.request_package["channel_name"] + ":" + recv_data) 
            
            if self.log:
                self.file.write(recv_data + "\n")

            return recv_data
        except:
            print("socket no loger connected or master not running")
            if self.sensor_soc:
                self.sensor_soc.close()
            return None
    
