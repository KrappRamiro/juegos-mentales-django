import json
from .mqtt import mqttc


def liberar_grillete(n_grillete):
    print(f"Liberando grillete #{n_grillete}")
    document = {
        "state": {
            "desired": {
                f"grillete_{n_grillete}": False
            }
        }
    }
    mqttc.publish(topic="$aws/things/grilletes/shadow/update",
                  payload=json.dumps(document), qos=1)


def on_message(client, userdata, message):
    # Do something
    print(" Received message " + str(message.payload)
          + " on topic '" + message.topic
          + "' with QoS " + str(message.qos))
    pass


def grilletes_callback(client, userdata, msg):
    pass


def soporte_cuchillos_callback(client, userdata, msg):
    pass


def luz_callback(client, userdata, msg):
    pass


def heladera_callback(client, userdata, msg):
    pass


def especiero_callback(client, userdata, msg):
    pass


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
    liberar_grillete(2)
