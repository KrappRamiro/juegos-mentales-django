import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform

connflag = False


def on_message(client, userdata, message):
    # Do something
    print(" Received message " + str(message.payload)
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("---------   Connected to MQTT Broker!   ---------")
    else:
        print("Failed to connect, return code %d\n", rc)
    global connflag
    connflag = True

    # ----------- Licuadora --------------- #
    client.subscribe("+/debug/#", 1)
    client.message_callback_add(
        "+/debug/#",
        callbacks.debug)


mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

print("Trying to connect with mqttc.connect")
mqttc.connect('localhost', 1883, keepalive=60)
print("Finished trying to connect to mqttc.connect")

# This is here to avoid circular imports
from . import callbacks
