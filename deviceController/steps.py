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


def licuadora(message={}, skip=False):
    def solve():
        actions.liberar_grillete(0)  # TODO: Ver que grillete se liberaba
    if skip:
        solve()
        return
    if message["estado_boton"] == True:
        solve()


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
    especieros = {
        "rfid_0": "3A 38 DA 80",
        "rfid_1": "6A EA 01 81",
        "rfid_2": "C9 33 1F 88",
        "rfid_3": "F9 A9 29 87"
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
        "rfid_0": "CA E5 EC 80",
        "rfid_1": "A3 9C D6 1B",
        "rfid_2": "00 00 00 00",
        "rfid_3": "5A 1C E5 80"
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
        actions.abrir_tablero_electrico()
    if skip:
        solve()
        return
    if message["rfid"] == "90 A3 FB 1B":
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
    pies = {
        "rfid_0": "AA 2F FD 80",
        "rfid_1": "49 88 29 87",
        "rfid_2": "79 10 22 A4",
        "rfid_3": "F9 67 13 87"
    }
    print(f"message = {message}")
    print(f"pies = {pies}")
    if message != pies:
        print("Wrong combination for pies")
        return
    print("Correct combination for pies")
    solve()


def teclado_heladera(tecla_in="", skip=False):
    def solve():
        actions.abrir_cajon("C2")

    if skip:
        solve()
        return
    clave = ['1', '1', '1', '2', '2', '1']
    print(f"La tecla introducida es la tecla {tecla_in}")
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

    print(f"El mensaje de la heladera es {message}")
    combinacion_llaves_paso = [False, False, False, False]
    if message["interruptores"] == True:
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
