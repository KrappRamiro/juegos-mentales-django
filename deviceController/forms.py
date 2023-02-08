from django import forms


class LightForm(forms.Form):
    brightness = forms.IntegerField(label="Nivel de brillo")
    flicker = forms.BooleanField(label="Parpadea?", required=False)


class LightsConfigurationForm(forms.Form):
    MODES_CHOICES = (
        ("fixed", "Modo fijo"),
        ("scary", "Modo Asustadizo"),
        ("panic", "Modo Panico (luces en rojo)"),
        ("off", "Luces apagadas")
    )
    mode = forms.ChoiceField(choices=MODES_CHOICES, label="Modo de las luces")
    fixed_brightness = forms.IntegerField(
        label="Nivel de brillo para el modo fijo"
    )
    flicker_min_time = forms.IntegerField(
        label="Tiempo mínimo entre parpadeos")
    flicker_max_time = forms.IntegerField(
        label="Tiempo máximo entre parpadeos")
    blackout_min_time = forms.IntegerField(
        label="Tiempo mínimo entre apagones")
    blackout_max_time = forms.IntegerField(
        label="Tiempo máximo entre apagones")
