# Name: Isaac Chang
# Date: June 17, 2018

import time
from source.sensor import Sensor
from source.sensorSubscriber import SensorSubscriber

def main():

    # declare sensor subscribers
    accel_sub = SensorSubscriber(channel_name="/accel/raw", log=True)

    # send data
    res = 1
    while res != None:
        # just for easier to see whats going on
        time.sleep(1)

        # sensor subs subscribe to data 
        res = accel_data_in = accel_sub.request_data()

        # print sensor data if you want
        #print(accel_data_in)

if __name__ == "__main__":
    main()

