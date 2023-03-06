from time import sleep
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LightForm, LightsConfigurationForm
import logging
from django.forms import formset_factory
from . import actions
from . import steps
from .mqtt import mqttc
import json
from .models import Step

logger = logging.getLogger(__name__)


def index(request):
    steps = Step.objects.all().order_by("id")
    context = {
        "steps": steps
    }
    return render(request, "deviceController/index.html", context)


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
    if not validness:
        return HttpResponse("Validation error in the forms :(")
    print("Everything validated just right")
    formset = formset.cleaned_data
    uv_light = uv_light.cleaned_data
    lights_config = lights_config.cleaned_data
    document = {
        "state": {
            "desired": {
                "config": lights_config,
                "rgb_lights": [
                    formset[0],
                    formset[1],
                    formset[2],
                    formset[3]
                ],
                'uv_light': uv_light
            }
        }
    }
    print("Publishing this document to AWS ligths shadow:")
    print(json.dumps(document, indent=4))
    mqttc.publish("$aws/things/luz/shadow/update",
                  payload=json.dumps(document), qos=1)
    sleep(0.5)
    return redirect(light_control)


def light_control(request):

    # Ask the mqtt-broker for information
    mqttc.publish("$aws/things/luz/shadow/get")
    sleep(1)  # Wait until the information is recieved
    from . import global_luz
    print(
        f"***** The global_luz is: ****** \n{json.dumps(global_luz,indent=4)}\n")
    # Proceed with the display of the data
    # Different initial data for each form in a Django formset https://stackoverflow.com/a/23497278/15965186
    LightFormSet = formset_factory(LightForm, extra=0)
    # Get the formset for the RGB Lights
    formset = LightFormSet(
        initial=[
            global_luz["rgb_lights"][0],
            global_luz["rgb_lights"][1],
            global_luz["rgb_lights"][2],
            global_luz["rgb_lights"][3]
        ])
    # Get the form for the UV Light
    uv_light = LightForm(
        initial=global_luz["uv_light"])
    # Get the form for the Light config
    lights_config = LightsConfigurationForm(initial=global_luz["config"])
    context = {
        "formset": formset,
        "uv_light_form": uv_light,
        "lights_config_form": lights_config
    }
    return render(request, "deviceController/light_control.html", context)


def skip_step(request, step_name):
    print("Se ha pedido skipear {}".format(step_name.replace("_", " ")))
    if step_name == "tablero_herramientas":
        steps.tablero_herramientas(skip=True)
    elif step_name == "luz":
        steps.luz(skip=True)
    elif step_name == "licuadora":
        steps.licuadora(skip=True)
    elif step_name == "especiero":
        steps.especiero(skip=True)
    elif step_name == "soporte_cuchillos":
        steps.soporte_cuchillos(skip=True)
    elif step_name == "soporte_pies":
        steps.soporte_pies(skip=True)
    elif step_name == "teclado_heladera":
        steps.teclado_heladera(skip=True)
    elif step_name == "cuadro":
        steps.cuadro(skip=True)
    elif step_name == "llaves_paso":
        steps.llaves_paso(skip=True)
    elif step_name == "caldera":
        steps.caldera(skip=True)
    else:
        print("ERROR!!! No se ha encontrado esa accion")

    return redirect(index)


def reset_game(request):
    print("Reseteando la sala")
    actions.reset_game()
    return redirect(index)


def liberar_grillete(request, grillete):
    print(f"Desde la web se pidio liberar el grillete {grillete}")
    actions.liberar_grillete(grillete)
    return redirect(index)


def abrir_cajon(request, cajon):
    print(f"Desde la web se pidio liberar el cajon {cajon}")
    actions.abrir_cajon(cajon)
    return redirect(index)


def iniciar_sala(request):
    actions.iniciar_radio()
    actions.iniciar_sistema_audio()
    return redirect(index)


def radio_vol_up(request):
    mqttc.publish(topic="radio/actions/vol_up")
    return redirect(index)


def radio_vol_down(request):
    mqttc.publish(topic="radio/actions/vol_down")
    return redirect(index)


def sistema_audio_vol_up(request):
    mqttc.publish(topic="sistema_audio/actions/vol_up")
    return redirect(index)


def sistema_audio_vol_down(request):
    mqttc.publish(topic="sistema_audio/actions/vol_down")
    return redirect(index)
