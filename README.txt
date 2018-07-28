Title: Sensors Platform

Author: Isaac Chang
Date: June 17, 2018

Python Version: 2.7.12

Intro:

This sensory framework is meant for interfacing between different physical devices, platforms and programs. 
It uses a simple TCP/IP server denoted as the "sensorMaster" which redirects requests from different sensors onto "channels" much like the ROS framework. 
It uses a generic dictionary/YAML data structure type allowing the user to customize the data type they want to send. While the sample data in the test.py is declared in dictionary form this can be easily changed to loading in from a YAML file.

The framework comprises of 3 main classes. The SensorMaster, Sensor, and SensorSubscriber.

The SensorMaster must be ran in advance to any programs using the latter 2 classes. It is the main server handling all data requests whether incoming or outgoing.
How it works:
    - It first spawns 2 major processes one which handles Sensor client connections and saves the incoming data to a shared memory space
    - The second which handles incoming SensorSubscriber client connections and sends back parts of the shared memory based on a channel name
    - Every time each major process handles a connection it starts a new thread, this is so multiple clients can be served concurrently
    - The main 2 processes never end no matter what clients disconnect, this means you can stop your sensor program, modify it and re-run it all with the sensor platform still running

The Sensor is the object declared when writing the program interfacing with the physical sensor. To instantiate a Sensor object you must give it a channel_name.
After doing so all that needs to be done is to create your dictionary type data type, insert your data and use the in-built "send_data" function.

The SensorSubscriber is the object declared when writing a program to process incoming sensor data. It provides functionality to read from an existing channel.
It also has an extra paramater allowing for logging on everything it receives on the channel. The log file can be specified but the default is set in the local "logs" directory

As shown any platform as long as it runs python and is TCP/IP compatible can operate on this framework.
Sending sensor data from one sensor to any other sensor or program is simple as all it requires from the user is knowledge of a channel name.
The framework however does rely on the user to not use conflicting channel names, this can be changed in the future by keeping a global list of channel names that is checked at channel creation. 

Notes:

The way the channels work is that they constantly clear buffer. What this means is that if the Sensor object is declared first and starts publishing to a channel previous to a subscriber subscribing.
The SensorSubscriber will not receive a huge queue of the data previous to it connecting. This was done to avoid latency on connection and for real time sensor data, if the subcriber side fails to process at the same speed as the Sensor producing the data then programs can't react to real-time scenarios.

Demo Run Instructions:

- Unzip the "ichang-ascent-sensors" directory somewhere on your host computer

1. Open 2 Terminals

2. Navigate to the "ichang-ascent-sensors" directory for both

3. In terminal 1 run "python sensorMaster.py"

4. Wait to see if the master comes up (it would be obvious as there's a print out)

-------------------------------------- Print Out -------------------------------------------------
Ascent Robotics Code Assignment: Sensor System
Type 'q' to close master and end all child processes
Sensor Master Listening for new client... 
Sensor Master requires both a sensor and subscriber connection within 120s otherwise it will timeout
-------------------------------------- Print Out -------------------------------------------------

- keep in mind, serverMaster.py will timeout in 120s if no client connections attach to it, this is to avoid an idle master

5. Once the master is up, go to terminal 2 and run "python test.py"

6. Terminal 1 (running sensorMaster.py) should be showing client connections
    - These are the 2 fake sensors (gyro, accelerometer) and 2 fake subscribers connecting to the sensorMaster

7. Terminal 2 (running test.py) should be showing the feedback from the respective Sensors and Subscribers
    - Fake data is used in the test and one variable in each dictionary is consistently increased to show change in data

*** At this point you are able to see the flow of data however, if you want to see flow into an entirely seperate process do the following:
- Open a third Terminal (Terminal 3)
- navigate to the "ichang-ascent-sensors" directory
- run "python test2.py"
- notice the incoming flow of accelerometer data

8. After allowing "test.py" to run on Terminal 2 for a while, feel free to ctrl+c out of it, notice that this does not kill the serverMaster.py task running on Terminal 1
    - You can disconnect and reconnect to the sensorsMaster as many times as you want without closing the program.
    - Feel free to modify test.py's data to increase by 2 instead 1 on line 42 and 43 of test.py and rerun the script in Terminal 2
    - Also, if you ran "test2.py" notice how in Terminal 3 it is indicating no channel is found
        - re-run "test.py" in Terminal 2 to see how "test2.py" picks right up on the new channel

9. To end the demo go onto Terminal 1 (serverMaster.py) and press 'q' then press 'Enter' once prompted

10. Lastly as part of the test I turned on the logging function of the subscribers so if you look under the 'logs' directory you will see new log files
    - feel free to "tail -f" these files to view as they are filled while running the processes above
    - also note even though "test2.py" and "test.py" logs to the same file based on channel name, log_file is a paramter that can be changed in the sensorSubscriber class
