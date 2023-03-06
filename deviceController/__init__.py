from .mqtt import mqttc

# https://stackoverflow.com/questions/41015779/how-to-use-paho-mqtt-client-in-django

mqttc.loop_start()
global_luz = {}


def mutate_luz(luz):
    global global_luz
    global_luz = luz
