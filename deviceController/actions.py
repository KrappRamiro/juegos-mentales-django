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


def publish_to_elements(thingname, subtopic, dictionary={}):
    topic = thingname + '/elements/' + subtopic
    print(f"Reporting to {topic} the following dictionary: {dictionary}")
    mqttc.publish(topic=topic, payload=json.dumps(dictionary), qos=1)


def liberar_grillete(n_grillete):
    print(f"Liberando grillete #{n_grillete}")
    publish_to_elements(
        "grilletes", f"electroiman_{n_grillete}", {"status": True})


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
    print(f"Abriendo cajon {cajon}")
    electroiman_n = cajon[1]
    publish_to_elements(
        "cajones_bajomesada", f"electroiman_{electroiman_n}", {"status": True})


def poner_luces_rojo():
    print("Poniendo las luces en rojo")
    document = {
        "config": {
            "mode": "panic"
        }
    }
    publish_to_elements("luz", "lights", document)


def abrir_caldera():
    print("Abriendo la caldera")
    document = {
        "electroiman_caldera": True
    }
    publish_to_elements("caldera", "electroiman_caldera", document)
    poner_luces_rojo()


def prender_luz():
    print("Prendiendo la luz")
    # Reminder: Its not needed to set the lightning level from here
    document = {
        "config": {
            "mode": "scary"
        }
    }
    publish_to_elements("luz", "lights", document)


def apagar_luz():
    print("Apagando la luz")
    document = {
        "config": {
            "mode": "off"
        }
    }
    publish_to_elements("luz", "lights", document)


def prender_luz_uv():
    print("Prendiendo la luz UV")
    document = {
        "uv_light": {
            "brightness": 250,
        }
    }
    publish_to_elements("luz", "lights", document)


def apagar_luz_uv():
    print("Apagando la luz UV")
    document = {
        "uv_light": {
            "brightness": 0,
        }
    }
    publish_to_elements("luz", "lights", document)


def abrir_heladera():
    print("Abriendo la heladera")
    document = {
        "status": True
    }
    publish_to_elements("heladera", "electroiman", document)


def abrir_tablero_electrico():
    print("Abriendo el tablero electrico")
    document = {
        "status": True
    }
    publish_to_elements("caldera", "electroiman_tablero", document)


def iniciar_radio():
    print("Reiniciando la radio")
    document = {
        "track_n": 1
    }
    publish_to_elements("radio", "track_n", document)


def iniciar_sistema_audio():
    print("Reiniciando el sistema audio")
    document = {
        "track_n": 1
    }
    publish_to_elements("sistema_audio", "track_n", document)


def reset_game():
    from . import actions
    from .models import Step
    try:
        steps = Step.objects.all()
        for step in steps:
            step.solved = False
            step.save()
    except Exception as e:
        print(e)
    actions.apagar_luz()
    # region reset electroimanes
    document = {
        "status": False
    }
    publish_to_elements("caldera", "electroiman_tablero", document)
    publish_to_elements("caldera", "electroiman_caldera", document)
    for e in range(4):
        publish_to_elements("grilletes", f"electroiman_{e+1}", document)
    for e in range(3):
        publish_to_elements("cajones_bajomesada",
                            f"electroiman_{e+1}", document)
    publish_to_elements("heladera", "electroiman", document)
    # endregion

    # region reset luz
    document = {
        "config": {
            "mode": "off",
        },
        "uv_light": {
            "brightness": 0
        }
    }
    publish_to_elements("luz", "lights", document)
    # endregion reset luz

    # region reset audio
    document = {
        "track_n": 0
    }
    publish_to_elements("radio", "track_n", document)
    publish_to_elements("sistema_audio", "track_n", document)
    # endregion

    # Reset the RFID memory
    mqttc.publish(topic="especiero/actions/clear_rfid")
    mqttc.publish(topic="cuadro/actions/clear_rfid")
    mqttc.publish(topic="soporte_pies/actions/clear_rfid")
    mqttc.publish(topic="tablero_herramientas/actions/clear_rfid")
