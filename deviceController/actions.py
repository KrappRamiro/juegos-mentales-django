"""_summary_
This file and it functions should only be used for:
    * Defining how the actions in the game are going to modify the devices
Dont use it for defining the steps of the game or handling the callbacks
Thats the job of steps.py and callbacks.py respectively

Example of action:

def liberar grillete(n_grillete):
    # Ask the grilletes device to release grillete n 2
    document = {
        "grillete_2": False
    }
    mqttc.publish("grilletes", document)

*** The actions in this file will be called by steps.py and other files if that is necessary ***
"""

import json
from .mqtt import mqttc


def desire_to_shadow(thingname, dictionary):
    print(
        f"Reporting to the shadow of {thingname} the following dictionary: {dictionary}")
    doc = {
        "state": {
            "desired": dictionary
        }
    }
    mqttc.publish(topic=f"$aws/things/{thingname}/shadow/update",
                  payload=json.dumps(doc), qos=1)


def liberar_grillete(n_grillete):
    print(f"Liberando grillete #{n_grillete}")
    document = {
        f"grillete_{n_grillete}": False
    }
    desire_to_shadow("grilletes", document)


def abrir_cajon(cajon):
    """_summary_
    # C1:
        Este cajon se abre después de colocar los especieros.

        Contiene una llave tuerca 10 de los grilletes del jugador No. 4, un cuchillo y un pie cortado 3.

    # C2: 
        Este cajon se deberia abrir cuando se resuelve el teclado numerico de la heladera

        Contiene parte de las instrucciones para configurar el panel eléctrico
        y en el reverso de la nota, vemos un catálogo de obras de arte,
        una de ellas cuelga en nuestra habitación

    # C3
        Este cajon se abre cuando damos vuelta el cuadro.

        Tiene una nota que dice:
        Señor, incluidas las subestaciones en este orden, el sistema comienza a actuar,
        no permita que los interruptores de palanca (térmicas) estén en esta posición
    """
    if cajon == "C1":
        document = {
            "electroiman_1": False
        }
    if cajon == "C2":
        document = {
            "electroiman_2": False
        }

    if cajon == "C3":
        document = {
            "electroiman_3": False
        }
    desire_to_shadow("cajones_bajomesada", document)


def poner_luces_rojo():
    print("Poniendo las luces en rojo")
    document = {
        "config": {
            "mode": "panic"
        }
    }
    desire_to_shadow("luz", document)


def abrir_caldera():
    print("Abriendo la caldera")
    document = {
        "electroiman_caldera": False
    }
    desire_to_shadow("caldera", document)
    poner_luces_rojo()


def prender_luz():
    print("Prendiendo la luz")
    # Reminder: Its not needed to set the lightning level from here
    document = {
        "config": {
            "mode": "scary"
        }
    }
    desire_to_shadow("luz", document)


def apagar_luz():
    print("Apagando la luz")
    document = {
        "config": {
            "fixed_brightness": 0,
            "mode": "fixed"
        }
    }
    desire_to_shadow("luz", document)


def prender_luz_uv():
    print("Prendiendo la luz UV")
    document = {
        "uv_light": {
            "brightness": 250,
        }
    }
    desire_to_shadow("luz", document)


def abrir_heladera():
    print("Abriendo la heladera")
    document = {
        "electroiman": False
    }
    desire_to_shadow("heladera", document)


def abrir_tablero_electrico():
    print("Abriendo el tablero electrico")
    document = {
        "electroiman_tablero_electrico": False
    }
    desire_to_shadow("caldera", document)


def reset_game():
    # TODO: Re-do this function
    """_summary_
    This function should publish an /update to all the shadows, with a
    {
        "state": {
            "desired": {
                ... : ...,
                ... : ...
            }
        }
    document, which contains the initial value of the sala
    """
    # region reset caldera
    document = {
        "state": {
            "desired": {
                "electroiman_caldera": True
            }
        }
    }
    mqttc.publish(topic="$aws/things/caldera/shadow/update",
                  payload=json.dumps(document), qos=1)
    # endregion reset caldera

    # region reset grilletes
    document = {
        "state": {
            "desired": {
                "grillete_1": True,
                "grillete_2": True,
                "grillete_3": True,
                "grillete_4": True
            }
        }
    }

    mqttc.publish(topic="$aws/things/grilletes/shadow/update",
                  payload=json.dumps(document), qos=1)
    # endregion reset grilletes

    # region reset luz
    document = {
        "state": {
            "desired": {
                "mode": "fixed",
                "fixed_brightness_level": 0,
                "uv_light_active": False,
                "uv_light_brightness": 0
            }
        }
    }
    mqttc.publish(topic="$aws/things/luz/shadow/update",
                  payload=json.dumps(document), qos=1)
    # endregion reset luz

    # region reset heladera
    document = {
        "state": {
            "desired": {
                "electroiman": True
            }
        }
    }
    mqttc.publish(topic="$aws/things/heladera/shadow/update",
                  payload=json.dumps(document), qos=1)
    # endregion reset heladera
