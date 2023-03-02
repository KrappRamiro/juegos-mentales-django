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


def heladera(client, userdata, msg):
    print("Handling heladera callback")
    message = json.loads(msg.payload.decode('utf-8'))
    tecla = message["key"]  # Get the inputted tecla
    steps.teclado_heladera(tecla)
