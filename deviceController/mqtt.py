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
    # client.subscribe("#", 1) #Suscribe to every topic, just for testing purposes
    # ----------- Tablero herramientas --------------- #
    client.subscribe("$aws/things/tablero_herramientas/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/tablero_herramientas/shadow/update",
        callbacks.tablero_herramientas)

    # ----------- Especiero --------------- #
    client.subscribe("$aws/things/especiero/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/especiero/shadow/update",
        callbacks.especiero)

    # ----------- Soporte cuchillos --------------- #
    client.subscribe("$aws/things/soporte_cuchillos/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/soporte_cuchillos/shadow/update",
        callbacks.soporte_cuchillos)

    # ----------- Soporte Pies --------------- #
    client.subscribe("$aws/things/soporte_pies/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/soporte_pies/shadow/update",
        callbacks.soporte_pies)

    # ----------- Teclado de la heladera --------------- #
    client.subscribe("heladera/teclado", 1)
    client.message_callback_add(
        "heladera/teclado",
        callbacks.heladera)

    # ----------- Caldera --------------- #
    client.subscribe("$aws/things/caldera/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/caldera/shadow/update",
        callbacks.caldera)

    # ----------- Luz --------------- #
    client.subscribe("luz/switch", 1)
    client.message_callback_add(
        "luz/switch",
        callbacks.luz)
    client.subscribe("$aws/things/luz/shadow/get/accepted", 1)
    client.message_callback_add(
        "$aws/things/luz/shadow/get/accepted",
        callbacks.luz_accepted)

    # ----------- Cuadro --------------- #
    client.subscribe("$aws/things/cuadro/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/cuadro/shadow/update",
        callbacks.cuadro)

    # ----------- Licuadora --------------- #
    client.subscribe("$aws/things/licuadora/shadow/update", 1)
    client.message_callback_add(
        "$aws/things/licuadora/shadow/update",
        callbacks.licuadora)


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
caPath = "/var/app/current/certificates/AmazonRootCA1.crt"
certPath = "/var/app/current/certificates/certificate.pem"
keyPath = "/var/app/current/certificates/private.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath,
              cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

print("Trying to connect with mqttc.connect")
# Change this when using real code
mqttc.connect_async(awshost, awsport, keepalive=60)
print("Finished trying to connect to mqttc.connect")

# This is here to avoid circular imports
from . import callbacks
