from django import forms


class LightConfigForm(forms.Form):
    MODES_CHOICES = (
        ("fixed", "Modo fijo"),
        ("scary", "Modo Asustadizo"),
        ("panic", "Modo Panico (luces en rojo)"),
        ("off", "Luces apagadas")
    )
    mode = forms.ChoiceField(choices=MODES_CHOICES, label="Modo de las luces")
    rgb_brightness = forms.IntegerField(
        label="Nivel de brillo de las luces")
    uv_brightness = forms.IntegerField(
        label="Nivel de brillo de la luz UV")
    flicker_min_time = forms.IntegerField(
        label="Tiempo mínimo entre parpadeos")
    flicker_max_time = forms.IntegerField(
        label="Tiempo máximo entre parpadeos")
    blackout_min_time = forms.IntegerField(
        label="Tiempo mínimo entre apagones")
    blackout_max_time = forms.IntegerField(
        label="Tiempo máximo entre apagones")
