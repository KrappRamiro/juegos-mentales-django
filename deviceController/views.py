from pymongo import MongoClient
from time import sleep
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LightForm, LightsConfigurationForm
import logging
from django.forms import formset_factory
from . import actions
from .mqtt import mqttc
import json
logger = logging.getLogger(__name__)


def update_lights(request):
    if request.method == "POST":
        print(
            f"\n------------------------------------------------------\nEl request.POST es:\n{request.POST} \n-----------------------------------------------------\n")
    LightFormSet = formset_factory(LightForm, extra=0)
    formset = LightFormSet(request.POST)
    uv_light = LightForm(request.POST)
    lights_config = LightsConfigurationForm(request.POST)
    validness = True
    if formset.is_valid() == False:
        print("Formset validation failed")
        print(formset.errors)
        print(formset.is_bound)
        validness = False
    if uv_light.is_valid() == False:
        print("UV light validation failed")
        validness = False
    if lights_config.is_valid() == False:
        print("Light configuration validation failed")
        validness = False
    if validness == False:
        return HttpResponse("Validation error in the forms :(")
    print("Everything validated just right")
    formset = formset.cleaned_data
    uv_light = uv_light.cleaned_data
    lights_config = lights_config.cleaned_data
    document = {
        "state": {
            "desired": {
                "led_lights": [
                    formset[0],
                    formset[1]
                ],
                "rgb_lights": [
                    formset[2],
                    formset[3]
                ],
                'uv_light_brightness_level': uv_light['brightness_level']
            }
        }
    }
    document["state"]["desired"].update(lights_config)
    print("Publishing this document to AWS ligths shadow:")
    print(json.dumps(document, indent=4))
    mqttc.publish("$aws/things/luz/shadow/update",
                  payload=json.dumps(document), qos=1)
    sleep(0.5)
    return redirect(index)


def index(request):
    # Ask the mqtt-broker for information
    mqttc.publish("$aws/things/luz/shadow/get")
    sleep(0.5)
    # Wait until the information is recieved
    from . import global_luz
    print(
        f"***** The global_luz is: ****** \n{json.dumps(global_luz,indent=4)}\n")
    # Proceed with the display of the data
    # Different initial data for each form in a Django formset https://stackoverflow.com/a/23497278/15965186
    LightFormSet = formset_factory(LightForm, extra=0)
    formset = LightFormSet(
        initial=[
            global_luz["led_lights"][0],
            global_luz["led_lights"][1],
            global_luz["rgb_lights"][0],
            global_luz["rgb_lights"][1]
        ])
    uv_light = LightForm(
        initial={"brightness_level": global_luz["uv_light_brightness_level"]})
    lights_config = LightsConfigurationForm(initial=global_luz
                                            )
    context = {
        "formset": formset,
        "uv_light_form": uv_light,
        "lights_config_form": lights_config
    }
    return render(request, "deviceController/index.html", context)


def skip_step(request, step_name):
    print("Se ha pedido skipear {}".format(step_name.replace("_", " ")))
    if step_name == "tablero_herramientas":
        actions.liberar_grillete(2)
    elif step_name == "licuadora":
        actions.liberar_grillete(1)
    elif step_name == "soporte_especieros":
        actions.liberar_grillete(4)
        actions.abrir_alacena_pared()
    elif step_name == "soporte_cuchillos":
        actions.prender_luz_uv()
    elif step_name == "soporte_pies":
        actions.abrir_heladera()
    elif step_name == "heladera":
        actions.abrir_cajon_alacena()
    elif step_name == "cuadro":
        actions.abrir_cajon_comoda()
        actions.abrir_tablero_electrico()
    elif step_name == "caldera":
        actions.abrir_caldera()
    else:
        print("ERROR!!! No se ha encontrado esa accion")

    return redirect(index)


def reset_game(request):
    print("Reseteando la sala")
    actions.reset_game()
    return redirect(index)
