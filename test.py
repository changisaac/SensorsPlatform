# Name: Isaac Chang
# Date: June 17, 2018

import time
from source.sensor import Sensor
from source.sensorSubscriber import SensorSubscriber

def main():

    # declare sensor objects
    accel_sensor = Sensor(channel_name="/accel/raw")
    gyro_sensor = Sensor(channel_name="/gyro/raw")

    # declare sensor subscribers
    accel_sub = SensorSubscriber(channel_name="/accel/raw", log=True)
    gyro_sub = SensorSubscriber(channel_name="/gyro/raw", log=True)

    # fake data
    accel_data = {"accel_x": 0, "accel_y": 0, "accel_z": 0}
    gyro_data = {"vel_x": 0, "vel_y": 0, "vel_z": 0}

    # send data
    res = 1
    while res:
        # sensors send data to master and master puts it on a channel
        res = accel_sensor.send_data(accel_data)
        res = gyro_sensor.send_data(gyro_data)

        # just for easier to see whats going on
        time.sleep(1)

        # sensor subs subscribe to data 
        accel_data_in = accel_sub.request_data()
        gyro_data_in = gyro_sub.request_data()

        # print recv data if you want to
        #print(accel_data_in)
        #print(gyro_data_in)

        # alter data to see change
        accel_data["accel_x"] += 1
        gyro_data["vel_y"] += 1


if __name__ == "__main__":
    main()

