import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform

connflag = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("---------   Connected to MQTT Broker!   ---------")
    else:
        print("Failed to connect, return code %d\n", rc)
    global connflag
    connflag = True
    client.subscribe("$aws/things/tablero_herramientas/shadow/update", 1)
    # client.subscribe("#", 1) #Suscribe to every topic, just for testing purposes
    client.message_callback_add(
        "$aws/things/tablero_herramientas/shadow/update",
        callbacks.tablero_herramientas)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))


mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
# mqttc.on_log = on_log

awshost = "a3df45vgz0yp2s-ats.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "randomData"
thingName = "randomData"
caPath = "certificates/AmazonRootCA1.crt"
certPath = "certificates/certificate.pem"
keyPath = "certificates/private.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath,
              cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

# This is here to avoid circular imports
from . import callbacks
