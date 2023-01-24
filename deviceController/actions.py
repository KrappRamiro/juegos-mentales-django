import json
from .mqtt import mqttc


def liberar_grillete(n_grillete):
    """_summary_

    Args:
        n_grillete (int): Numero de grillete a liberar
    """
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


def abrir_alacena_pared():
    """_summary_
    esta alacena contiene una llave tuerca 10 de los grilletes del jugador No. 4, un cuchillo y un pie cortado 3.
    """


def abrir_cajon_alacena():
    """_summary_
    Este cajon se deberia abrir cuando se resuelve el teclado numerico de la heladera
    Contiene parte de las instrucciones para configurar el panel eléctrico
    y en el reverso de la nota, vemos un catálogo de obras de arte,
    una de ellas cuelga en nuestra habitación
    """
    print("Abriendo el PRIMER cajon bajomesada con instrucciones para panel electrico")


def abrir_cajon_comoda():
    """_summary_
    Este cajon se abre cuando damos vuelta el cuadro. Tiene una nota que dice:
    Señor, incluidas las subestaciones en este orden, el sistema comienza a actuar,
    no permita que los interruptores de palanca (térmicas) estén en esta posición
    """


def poner_luces_rojo():
    print("Poniendo las luces en rojo")
    document = {
        "state": {
            "desired": {
                "mode": "panic"
            }
        }
    }
    mqttc.publish(topic="$aws/things/luz/shadow/update",
                  payload=json.dumps(document), qos=1)


def abrir_caldera():
    print("Abriendo la caldera")
    document = {
        "state": {
            "desired": {
                "electroiman_caldera": False
            }
        }
    }
    mqttc.publish(topic="$aws/things/caldera/shadow/update",
                  payload=json.dumps(document), qos=1)
    poner_luces_rojo()


def prender_luz_uv():
    print("Prendiendo la luz UV")
    document = {
        "state": {
            "desired": {
                "uv_light_brightness_level": "200",
                "uv_light_active": True
            }
        }
    }
    mqttc.publish(topic="$aws/things/luz/shadow/update",
                  payload=json.dumps(document), qos=1)


def abrir_heladera():
    print("Abriendo la heladera")
    document = {
        "state": {
            "desired": {
                "electroiman": False
            }
        }
    }
    mqttc.publish(topic="$aws/things/heladera/shadow/update",
                  payload=json.dumps(document), qos=1)


def abrir_tablero_electrico():
    print("Abriendo el tablero electrico")
    document = {
        "state": {
            "desired": {
                "electroiman_tablero_electrico": False
            }
        }
    }
    mqttc.publish(topic="$aws/things/caldera/shadow/update",
                  payload=json.dumps(document), qos=1)


def reset_game():
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
