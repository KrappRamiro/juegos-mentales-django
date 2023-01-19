from django import forms


class DeviceForm(forms.Form):
    name = forms.CharField(label="Nombre del Objeto")


class PropertyForm(forms.Form):
    name = forms.CharField(label="Nombre de la propiedad")
    value = forms.CharField(label="Valor de la propiedad")
