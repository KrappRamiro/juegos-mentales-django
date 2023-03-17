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

# region helper functions


def check_rfid(input, expected):
    print(f"comparing \n{input} against \n{expected}")
    try:
        if input == expected:
            print("Correct RFID combination")
            return True
        else:
            print("Wrong RFID combination")
            return False
    except Exception as e:
        print(f"EXCEPTION!!!:\t{e}")


def check_switch(input):
    print("checking switch")
    try:
        return input["switch"]
    except Exception as e:
        print(f"EXCEPTION!!!:\t{e}")


def solve_step(name):
    from .models import Step
    print(f"Solving step {name}")
    try:
        step = Step.objects.get(step_name=name)
        step.solved = True
        step.save()
    except Exception as e:
        print(f"EXCEPTION!!!:\t{e}")


def check_step_solved(name):
    from .models import Step
    try:
        step = Step.objects.get(step_name=name)
    except Exception as e:
        print(f"EXCEPTION!!!:\t{e}")
    if step.solved:
        print(f"Step {name} is solved")
        return True
    else:
        print(f"Step {name} is not solved")
        return False
# endregion


def luz_switch(message={}, skip=False):
    def solve():
        actions.prender_luz()
        solve_step("luz")
    if skip:
        solve()
        return
    if check_step_solved("llaves_paso") == True:
        print("Not solving luz_switch because the lights have to be red")
        return
    if check_switch(message):
        solve()


def licuadora(message={}, skip=False):
    def solve():
        actions.liberar_grillete(3)
        solve_step("licuadora")

    if skip:
        solve()
        return
    if check_switch(message):
        solve()


def soporte_cuchillos(message={}, skip=False):
    def solve():
        actions.prender_luz_uv()
        solve_step("soporte_cuchillos")

    if skip:
        solve()
        return
    if check_switch(message):
        solve()


def especiero(message={}, skip=False):
    def solve():
        # actions.liberar_grillete(4) # Se libera usando candado de forma manual
        actions.abrir_cajon("C1")
        solve_step("especiero")

    if skip:
        solve()
        return
    combination = {
        "rfid_0": "F9 A9 29 87",
        "rfid_1": "6A EA 01 81",
        "rfid_2": "3A 38 DA 80",
        "rfid_3": "C9 33 1F 88"
    }
    if check_rfid(message, combination):
        solve()


def tablero_herramientas(message={}, skip=False):
    def solve():
        actions.liberar_grillete(1)
        solve_step("tablero_herramientas")

    if skip:
        solve()
        return
    combination = {
        "rfid_0": "CA E5 EC 80",
        "rfid_1": "59 C7 A4 A3",
        "rfid_2": "00 00 00 00",
        "rfid_3": "5A 1C E5 80"
    }
    if check_rfid(message, combination):
        solve()


def cuadro(message={}, skip=False):
    def solve():
        actions.abrir_cajon("C3")
        solve_step("cuadro")

    if skip:
        solve()
        return
    if check_step_solved("teclado_heladera") == False:
        return
    combination = {
        "rfid_0" == "90 A3 FB 1B"
    }
    if check_rfid(message, combination):
        solve()


def soporte_pies(message={}, skip=False):
    def solve():
        actions.abrir_heladera()
        actions.apagar_luz_uv()
        solve_step("soporte_pies")

    if skip:
        solve()
        return
    combination = {
        "rfid_0": "AA 2F FD 80",
        "rfid_1": "49 88 29 87",
        "rfid_2": "79 10 22 A4",
        "rfid_3": "F9 67 13 87"
    }
    if check_rfid(message, combination):
        solve()


def teclado_heladera(tecla_in="", skip=False):
    def solve():
        actions.abrir_cajon("C2")
        solve_step("teclado_heladera")

    if skip:
        solve()
        return
    clave = ['1', '1', '1', '2', '2', '1']
    print(f"La tecla introducida es la tecla {tecla_in}")
    teclas.append(tecla_in)
    if list(teclas) == clave:
        print("Clave correcta!!!")
        solve()


def llaves_paso(message={}, skip=False):
    def solve():
        actions.abrir_tablero_electrico()
        actions.poner_luces_rojo()
        solve_step("llaves_paso")
    if skip:
        solve()
        return
    if check_step_solved("cuadro") == False:
        print("Not solving llaves_paso because cuadro is not solved")
        return
    if message["llaves_paso"][1] == True and message["llaves_paso"][3] == True:
        solve()


def caldera(message={}, skip=False):
    def solve():
        actions.abrir_caldera()
        actions.poner_luces_rojo()
        solve_step("caldera")

    if skip:
        solve()
        return

    if check_step_solved("llaves_paso") == False:
        return
    should_solve = True

    if message["interruptores"] == False:
        print("interruptores: WRONG")
        should_solve = False
    else:
        print("interruptores: CORRECT")

    if message["atenuadores"] != [True, True]:
        print("atenuadores: WRONG")
        should_solve = False
    else:
        print("atenuadores: CORRECT")

    if message["botones"] == False:
        print("botones: WRONG")
        should_solve = False
    else:
        print("botones: CORRECT")

    if should_solve:
        solve()
