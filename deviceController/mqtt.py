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

    # ------------------- Debug -------------------- #
    client.subscribe("+/debug/#", 1)
    client.message_callback_add(
        "+/debug/#",
        callbacks.debug)
    # ------------------- rfid devices -------------------- #
    client.subscribe("+/readings/rfid")
    client.message_callback_add("+/readings/rfid", callbacks.rfid)
    # ------------------- switch devices -------------------- #
    client.subscribe("+/readings/switch")
    client.message_callback_add("+/readings/switch", callbacks.switch)
    # ----------------- heladera -------------------------- #
    client.subscribe("heladera/readings/keypad")
    client.message_callback_add("heladera/readings/keypad", callbacks.heladera)
    # ----------------- caldera -------------------------- #
    client.subscribe("caldera/readings/tablero_electrico")
    client.message_callback_add(
        "caldera/readings/tablero_electrico", callbacks.caldera)
    # ----------------- llaves_paso ----------------------- #
    client.subscribe("caldera/readings/llaves_paso")
    client.message_callback_add(
        "caldera/readings/llaves_paso", callbacks.llaves_paso)
    # ------------------ Light info for the webapp ------------------ #
    client.subscribe("luz/elements/#")
    client.message_callback_add(
        "luz/elements/#", callbacks.luz_elements)


mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

print("Trying to connect with mqttc.connect")
mqttc.connect('192.168.0.52', 1883, keepalive=60)
print("Finished trying to connect to mqttc.connect")

# This is here to avoid circular imports
from . import callbacks
