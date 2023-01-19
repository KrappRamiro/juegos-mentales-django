from pymongo import MongoClient
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import formset_factory
from .forms import DeviceForm, PropertyForm
import logging
logger = logging.getLogger(__name__)
mongo_client = MongoClient()

db = mongo_client.posts


def index(request):
    return HttpResponse("Hello, world. You're at the device controller index")


def add_device(request):
    PropertyFormSet = formset_factory(PropertyForm, extra=2)
    formset = PropertyFormSet()
    form = DeviceForm()
    if request.method == "POST":
        form = DeviceForm(request.POST)
        formset = PropertyFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            logging.info("Both form and formset were valid")
            form = form.cleaned_data
            object_name = form["name"]
            print(object_name)
            for f in formset:
                f = f.cleaned_data
                if f == {}:
                    continue
                print("Name: {} \t Value: {}".format(f["name"], f["value"]))
                print(f)

        else:
            logging.error("One of them was not valid")

    context = {'form': form, 'formset': formset}
    return render(request, 'deviceController/add_device.html', context)
