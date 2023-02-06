from .mqtt import mqttc
from pymongo import MongoClient

# https://stackoverflow.com/questions/41015779/how-to-use-paho-mqtt-client-in-django

mqttc.loop_start()
global_luz = {}

global_flag_luz_prendida = False


def activar_flag_luz_prendida():
    global global_flag_luz_prendida
    global_flag_luz_prendida = True


def retornar_flag_luz_prendida():
    global global_flag_luz_prendida
    return global_flag_luz_prendida


def desactivar_flag_luz_prendida():
    global global_flag_luz_prendida
    global_flag_luz_prendida = False


def mutate_luz(luz):
    global global_luz
    global_luz = luz
