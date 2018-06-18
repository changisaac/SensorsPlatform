# Name: Isaac Chang
# Date: June 17, 2018

import os
import sys
import socket
import json
import time

class Sensor:

    def __init__(self, channel_name):

        # sensor configs
        self.master_port = 8000
        self.max_recv_bytes = 1024

        # setup sensor sockets
        self.sensor_soc = socket.socket()
        self.host = socket.gethostname()

        try:
            self.sensor_soc.connect((self.host, self.master_port))
        except socket.error:
            return

        self.sensor_soc.settimeout(3)

        self.data_package = {"channel_name": channel_name}

    def send_data(self, data):

        try:
            self.data_package["data_value"] = data
            self.sensor_soc.send(json.dumps(self.data_package))
            echo = self.sensor_soc.recv(self.max_recv_bytes)
            print("published on channel " + self.data_package["channel_name"] + ": " + echo)
            return 1
        except:
            print("socket no longer connected or master not running")
            if self.sensor_soc:
                self.sensor_soc.close()
            return None

            
