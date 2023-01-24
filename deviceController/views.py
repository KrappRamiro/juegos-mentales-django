from pymongo import MongoClient
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import formset_factory
from .forms import DeviceForm, PropertyForm
import logging
from . import actions
logger = logging.getLogger(__name__)
mongo_client = MongoClient()

db = mongo_client.posts


def index(request):
    return render(request, "deviceController/index.html")


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
