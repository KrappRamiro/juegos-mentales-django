"""_summary_
This file and its functions should only be used for:
    * handling the callbacks
    * Processing their data
    * Calling other functions that can make use of that data
Dont intend to use it for making the steps of the game or defining how the actions in the game are going to modify the devices
Thats the job of steps.py and actions.py respectively
"""
import json
from .mqtt import mqttc
from . import actions
from . import steps


def debug(client, userdata, msg):
    topic = msg.topic.split('/')
    thingname = topic[0]
    subtopic = topic[2]
    message = msg.payload.decode('utf-8')
    print(f"{thingname} [{subtopic}] says: {message}")


def rfid(client, userdata, msg):
    print("Handling generic RFID callback")
    message = json.loads(msg.payload.decode('utf-8'))
    thingname = msg.topic.split('/')[0]
    if thingname == "especiero":
        steps.especiero(message)
    if thingname == "tablero_herramientas":
        steps.tablero_herramientas(message)
    if thingname == "soporte_pies":
        steps.soporte_pies(message)
    if thingname == "cuadro":
        steps.cuadro(message)


def switch(client, userdata, msg):
    print("Handling generic switch callback")
    message = json.loads(msg.payload.decode('utf-8'))
    thingname = msg.topic.split('/')[0]
    if thingname == "licuadora":
        steps.licuadora(message)
    if thingname == "soporte_cuchillos":
        steps.soporte_cuchillos(message)
    if thingname == "luz":
        steps.luz(message)


def heladera(client, userdata, msg):
    print("Handling heladera callback")
    message = json.loads(msg.payload.decode('utf-8'))
    tecla = message["key"]  # Get the inputted tecla
    steps.teclado_heladera(tecla)


def caldera(client, userdata, msg):
    print("Handling caldera callback")
    message = json.loads(msg.payload.decode('utf-8'))
    steps.caldera(message)


def llaves_paso(client, userdata, msg):
    print("Handling llaves_paso callback")
    message = json.loads(msg.payload.decode('utf-8'))
    steps.llaves_paso(message)
