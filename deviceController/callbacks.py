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
    print(f"The light message is {message}")
    if "switch_status" not in message:
        print("Not doing anything in luz callback cause there is no switch_status to interact with")
        return
    if message["switch_status"] == True:
        actions.prender_luz()
    if message["switch_status"] == False:
        actions.apagar_luz()


def soporte_cuchillos(client, userdata, msg):
    print("Handling soporte_cuchillos callback")
    # Process the payload
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    # Call the step
    steps.soporte_cuchillos(message)


def especiero(client, userdata, msg):
    print("Handling especiero callback")
    # decode the message into a python dictionary
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.soporte_especieros(message)


def tablero_herramientas(client, userdata, msg):
    print("Handling tablero_herramientas callback")
    # decode the message into a python dictionary
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.tablero_herramientas(message)


def soporte_pies(client, userdata, msg):
    print("Handling soporte_pies callback")
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    steps.soporte_pies(message)


def heladera(client, userdata, msg):
    print("Handling heladera callback")
    message = json.loads(msg.payload.decode('utf-8'))
    # Should not be needed because its not a shadow
    # if "desired" in message["state"]:
    #     return
    tecla = message["key"]  # Get the inputted tecla
    steps.teclado_heladera(tecla)


def caldera(client, userdata, msg):
    print("Handling caldera callback")
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    message = message["state"]["reported"]
    if "electroiman_caldera" in message:
        return
    if "electroiman_tablero" in message:
        return
    steps.caldera(message)


def licuadora(client, userdata, msg):
    print("Handling licuadora callback")
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    steps.licuadora(message)


def cuadro(client, userdata, msg):
    print("Handling cuadro callback")
    message = json.loads(msg.payload.decode('utf-8'))
    if "desired" in message["state"]:
        return
    steps.cuadro(message)
