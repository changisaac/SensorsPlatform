# Name: Isaac Chang
# Date: June 17, 2018

import os
import sys
import subprocess
import socket
import json
import multiprocessing as mp
import copy
import signal

class SensorMaster:

    def __init__(self):
       
        # sensor platform configs
        self.max_recv_bytes = 1024
        self.max_sensors = 10
        self.max_subscribers = 100

    def execute(self):
        
        # intro message
        print("Ascent Robotics Code Assignment: Sensor System")
        
        # initialize shared memory space within sensors master
        manager = mp.Manager()
        datums = manager.dict()
        
        # kill all flag in shared memory
        datums["kill"] = 0
        
        # start sensor master process
        # handles incoming sensors(clients) and updates sensor master's shared memory space with new sensor data
        self.master_proc = mp.Process(target=self.start_sensor_master, args=(datums,))
        self.master_proc.start()
       
        # start sensor data channels process
        # handles updated data from sensors and spawns a new server which outputs that sensor data
        self.data_proc = mp.Process(target=self.start_sensor_data, args=(datums,))
        self.data_proc.start() 

        # allow for user to kill test master and close port connections to sensors(clients)
        user_input = None 
        while user_input != 'q':
            user_input = raw_input("Type 'q' to close master and end all child processes\n")
        
        # update global kill all flag to end processes
        datums["kill"] = 1

        self.terminate()

    def terminate(self):
    
        print("Now Ctrl+c to exit (dont worry about the keyboard interrupt, I just didn't have time to catch catch the interrupt)")
        self.master_proc.join()
        self.data_proc.join()
        
        print("Sensors Platform Terminated")

    #=====================================================================================
    # Helper Functions
    #=====================================================================================

    def start_sensor_data(self, datums):

        data_port = 8001
        data_host = '0.0.0.0'
        data_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        data_soc.bind((data_host, data_port))
        
        data_soc.listen(self.max_subscribers)
        data_soc.settimeout(120)

        data_procs = list()
        while True:
            try:
                conn, addr = data_soc.accept()
            except:
                break
            data_soc.settimeout(None)
            data_proc = mp.Process(target=self.spawn_sensor_subscriber, args=(conn, addr, datums))
            data_proc.start()
            data_procs.append(data_proc)
       
        if data_procs != None:
            for data_proc in data_procs:
                data_proc.join()
        else:
            datums["kill"] = 0

    def start_sensor_master(self, datums):

        port = 8000
        host = '0.0.0.0'
        master_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        master_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        master_soc.bind((host, port))

        master_soc.listen(self.max_sensors)
        print("Sensor Master Listening for new client... ")
        print("Sensor Master requires both a sensor and subscriber connection within 60s otherwise it will timeout")
        master_soc.settimeout(60)

        procs = list()
        while True:
            try:
                conn, addr = master_soc.accept()
            except:
                break
            master_soc.settimeout(None)
            sensor_proc = mp.Process(target=self.spawn_sensor_channel, args=(conn, addr, datums))
            sensor_proc.start()
            procs.append(sensor_proc)

        if procs != None:
            for proc in procs:
                proc.join()
        else:
            datums["kill"] = 0

    def spawn_sensor_subscriber(self, conn, addr, datums):
        print("data connected to client at: " + str(addr))

        while not datums["kill"]:
            data = conn.recv(self.max_recv_bytes)
            
            try:
                data_load = json.loads(data)
            except ValueError:
                break

            # get channel name
            channel_name = data_load["channel_name"]

            # send shared memory space values to subscriber
            if str(channel_name) in datums:
                data_serialized = json.dumps(datums[str(channel_name)].copy())
                conn.send(data_serialized)
            # no channel set up
            else:
                conn.send("no channel by that name")

        conn.send("connection to sensors data terminated")
        conn.close()
        print("client connection at " + str(addr) + " closed")
    
    def spawn_sensor_channel(self, conn, addr, datums):
        print("master connected to client at: " + str(addr))
        channel_name = None

        while not datums["kill"]:
            data = conn.recv(self.max_recv_bytes)
            try:
                data_load = json.loads(data)
            except ValueError:
                break
            
            # get channel name and data value
            channel_name = data_load["channel_name"]
            data_value = data_load["data_value"]

            #update shared memory
            datums[channel_name] = data_value

            # echo back data
            conn.send(json.dumps(datums[channel_name].copy()))

        del datums[channel_name]
        conn.send("connection to sensors master terminated")
        conn.close()
        print("client connection at " + str(addr) + " closed")

def main():
    sensor_master = SensorMaster()
    sensor_master.execute()

if __name__ == "__main__":
    main()
