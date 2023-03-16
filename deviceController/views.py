from time import sleep
from django.shortcuts import render, redirect
import logging
from django.forms import formset_factory
from . import actions
from . import steps
from .mqtt import mqttc
import json
from .models import Step, LightConfig
from .forms import LightConfigForm
from django.forms.models import model_to_dict

logger = logging.getLogger(__name__)


def index(request):
    steps = Step.objects.all().order_by("id")
    context = {
        "steps": steps
    }
    return render(request, "deviceController/index.html", context)


def update_lights(request):
    from .actions import publish_to_elements
    if request.method == "POST":
        try:
            model = model_to_dict(LightConfig.objects.get())
        except Exception as e:
            print(f"EXCEPTION!!!:\t{e}")
        # initial=model is used later to see what fields have changed
        form = LightConfigForm(request.POST, initial=model)
        if form.is_valid():
            form_data = form.cleaned_data
            # Uncomment this if you want only the changed elements to be published
            '''
            changed_fields = form.changed_data
            new_dict = {
                key: value for (key, value) in form_data.items() if key in changed_fields}
            form_data = new_dict
            '''
            for key, value in form_data.items():
                publish_to_elements("luz", key, {key: value})
        else:
            print(form.errors)
        return redirect(light_control)


def light_control(request):
    sleep(0.3)
    # Get the form for the UV Light
    try:
        model = model_to_dict(LightConfig.objects.get())
    except Exception as e:
        print(f"EXCEPTION!!!:\t{e}")

    light_form = LightConfigForm(initial=model)
    context = {
        "light_form": light_form
    }
    return render(request, "deviceController/light_control.html", context)


def skip_step(request, step_name):
    print("Se ha pedido skipear {}".format(step_name.replace("_", " ")))
    if step_name == "tablero_herramientas":
        steps.tablero_herramientas(skip=True)
    elif step_name == "luz":
        steps.luz_switch(skip=True)
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
