import json
from .mqtt import mqttc
from collections import deque
from . import actions
# teclas is used in heladera callback
teclas = deque(6 * ['0'], 6)  # six 6, maxlen = 6


def on_message(client, userdata, message):
    # Do something
    print(" Received message " + str(message.payload)
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))
    pass


def abrir_heladera():
    print("Abriendo heladera")
    document = {
        "state": {
            "desired": {
                "electroiman": False
            }
        }
    }
    mqttc.publish(topic="$aws/things/heladera/shadow/update",
                  payload=json.dumps(document), qos=1)


def soporte_cuchillos(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    message = message["state"]["reported"]
    if message["estado_switch"] != True:
        return
    actions.prender_luz_uv()


def especiero(client, userdata, msg):
    especieros = {
        "rfid_0": "93 4E E3 1B",
        "rfid_1": "24 DD C5 DB",
        "rfid_2": "F3 FB 59 9B",
        "rfid_3": "33 61 E6 1B"
    }
    # decode the message into a python dictionary
    message = json.loads(msg.payload.decode('utf-8'))
    message = message["state"]["reported"]
    if message != especieros:
        print("Wrong combination for especieros")
        return
    print("Correct combination for especieros")
    # Este va al electroiman de la alacena que tiene la llave tuerca para el jugador 4
    actions.liberar_grillete(4)
    actions.abrir_alacena_pared()


def tablero_herramientas(client, userdata, msg):
    herramientas = {
        "rfid_0": "93 4E E3 1B",
        "rfid_1": "24 DD C5 DB",
        "rfid_2": "F3 FB 59 9B",
        "rfid_3": "33 61 E6 1B"
    }
    # decode the message into a python dictionary
    message = json.loads(msg.payload.decode('utf-8'))
    message = message["state"]["reported"]
    if message != herramientas:
        print("Wrong combination for herramientas")
        return
    print("Correct combination for herramientas")
    actions.liberar_grillete(2)


def soporte_pies(client, userdata, msg):
    pies = {
        "rfid_0": "93 4E E3 1B",
        "rfid_1": "24 DD C5 DB",
        "rfid_2": "F3 FB 59 9B",
        "rfid_3": "33 61 E6 1B"
    }
    message = json.loads(msg.payload.decode('utf-8'))
    message = message["state"]["reported"]
    message = message["state"]["reported"]
    if message != pies:
        print("Wrong combination for pies")
        return
    print("Correct combination for pies")
    abrir_heladera()


def heladera(client, userdata, msg):
    clave = ['1', '1', '1', '2', '2', '1']
    message = json.loads(msg.payload.decode('utf-8'))
    tecla = message["key"]
    teclas.append(tecla)
    print(list(teclas))
    if list(teclas) == clave:
        print("Clave correcta!!!")
        actions.abrir_cajon_alacena()
        actions.abrir_tablero_electrico()


def caldera(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    message = message["state"]["reported"]
    if (
        message["proximidad_1"] == True and
        message["proximidad_2"] == False and
        message["proximidad_3"] == True and
        message["proximidad_4"] == False and
        message["atenuador_1"] == True and
        message["atenuador_2"] == True and
        message["interruptor_1"] == False and
        message["interruptor_2"] == False
    ):
        actions.abrir_caldera()


def caldera(client, userdata, msg):
    # TODO
    print("Not yet implemented")
