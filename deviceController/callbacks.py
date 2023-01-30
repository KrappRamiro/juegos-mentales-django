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
# teclas is used in heladera callback


def luz_accepted(client, userdata, msg):
    # Callback for the shadow luz/get/accepted
    # Its used for getting the data for the webapp
    # This callback is an exception to the rule on how callbacks, actions and steps work in this project
    from . import mutate_luz
    print("Aceptada la luz")
    message = json.loads(msg.payload.decode('utf-8'))
    message = message["state"]["desired"]
    mutate_luz(message)


def luz(client, userdata, msg):
    # This function is for handling the on/off of the light via switch
    # This callback is an exception to the rule on how callbacks, actions and steps work in this project
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    if "estado_switch" not in message:
        print("Not doing anything in luz callback cause its just reporting its state")
        return
    if message["estado_switch"] == True:
        actions.prender_luz()
    if message["estado_switch"] == False:
        actions.apagar_luz()


def soporte_cuchillos(client, userdata, msg):
    print("Callback from soporte_cuchillos")
    # Process the payload
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    # Call the step
    steps.soporte_cuchillos(message)


def especiero(client, userdata, msg):
    # decode the message into a python dictionary
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.soporte_especieros(message)


def tablero_herramientas(client, userdata, msg):
    # decode the message into a python dictionary
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.tablero_herramientas(message)


def soporte_pies(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.soporte_pies()


def heladera(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    tecla = message["key"]  # Get the inputted tecla
    steps.teclado_heladera(tecla)


def caldera(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.caldera(message)
