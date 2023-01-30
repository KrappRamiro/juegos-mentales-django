"""_summary_
This file and it functions should only be used for:
    * Defining the order of the steps in the game
Dont use it for defining how the actions will modify the devices or handling the callbacks
Thats the job of actions.py and callbacks.py respectively

Example of step:

def step_licuadora():
    def solve():
        asustar_jugadores()
        liberar_grillete(3)
        abrir_heladera()

    if condition or skip:
        solve()


def step_especieros():
    def solve():
        liberar_jugador(5)
    
    if skip:
        solve()
    if especiero1 == "AA BB CC DD":
        print("Correct")
        solve()
"""
from . import actions
from collections import deque
teclas = deque(6 * ['0'], 6)  # six 6, maxlen = 6


def soporte_cuchillos(message={}, skip=False):
    def solve():
        actions.prender_luz_uv()

    if skip:
        solve()
        return
    if message["estado_switch"] is True:
        solve()


def soporte_especieros(message={}, skip=False):
    def solve():
        actions.liberar_grillete(4)
        actions.abrir_cajon("C1")

    if skip:
        solve()
        return
    especieros = {  # TODO: Change the RFID to the corresponding one
        "rfid_0": "93 4E E3 1B",
        "rfid_1": "24 DD C5 DB",
        "rfid_2": "F3 FB 59 9B",
        "rfid_3": "33 61 E6 1B"
    }
    if message != especieros:
        print("Wrong combination for especieros")
        return
    print("Correct combination for especieros")
    solve()
    # Este va al electroiman de la alacena que tiene la llave tuerca para el jugador 4


def tablero_herramientas(message={}, skip=False):
    def solve():
        actions.liberar_grillete(2)

    if skip:
        solve()
        return
    herramientas = {
        "rfid_0": "93 4E E3 1B",
        "rfid_1": "24 DD C5 DB",
        "rfid_2": "F3 FB 59 9B",
        "rfid_3": "33 61 E6 1B"
    }
    if message != herramientas:
        print("Wrong combination for herramientas")
        return
    print("Correct combination for herramientas")
    solve()


def licuadora(message={}, skip=False):
    def solve():
        actions.liberar_grillete(3)
    if skip:
        solve()
        return
    if message["boton"] == True:
        solve()


def cuadro(message={}, skip=False):
    def solve():
        actions.abrir_cajon("C3")
    if skip:
        solve()
        return
    # TODO: Change the RFID to the corresponding one
    if message["rfid"] == "AA BB CC DD":
        print("Cuadro is in the correct position")
        solve()
    else:
        print("Cuadro is NOT in the correct position")


def soporte_pies(message={}, skip=False):
    def solve():
        actions.abrir_heladera()

    if skip:
        solve()
        return
    pies = {  # TODO: Change the RFID to the corresponding one

        "rfid_0": "93 4E E3 1B",
        "rfid_1": "24 DD C5 DB",
        "rfid_2": "F3 FB 59 9B",
        "rfid_3": "33 61 E6 1B"
    }
    if message != pies:
        print("Wrong combination for pies")
        return
    print("Correct combination for pies")
    solve()


def teclado_heladera(tecla_in="", skip=False):
    def solve():
        actions.abrir_cajon("C2")
        actions.abrir_tablero_electrico()

    if skip:
        solve()
        return
    clave = ['1', '1', '1', '2', '2', '1']
    teclas.append(tecla_in)
    if list(teclas) == clave:
        print("Clave correcta!!!")
        solve()


def caldera(message={}, skip=False):
    def solve():
        actions.abrir_caldera()

    if skip:
        solve()
        return
    combinacion_interruptores = [True, False, True,
                                 False, False, False, True, False, False, False]
    combinacion_llaves_paso = [True, True, True, True]
    if message["interruptores"] != combinacion_interruptores:
        print("Los interruptores estan mal")
        return
    print("Los interruptores estan bien")
    if message["llaves_paso"] != combinacion_llaves_paso:
        print("Las llaves paso estan mal")
        return
    print("Las llaves paso estan bien")
    # El nivel de estos esta hardcodeado en el micro
    if message["atenuadores"] != [True, True]:
        print("Los atenuadores estan mal")
        return
    print("Los atenuadores estan bien")
    if message["botones"] != True:  # Estan hardcodeados en el cableado
        print("Los botones estan mal")
        return
    print("Los botones estan bien")
    solve()
