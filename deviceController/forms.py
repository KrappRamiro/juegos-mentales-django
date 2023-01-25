from django import forms


class LightForm(forms.Form):
    brightness_level = forms.IntegerField(label="Nivel de brillo")
    has_to_flicker = forms.BooleanField(label="Parpadea?", required=False)


class LightsConfigurationForm(forms.Form):
    MODES_CHOICES = (
        ("fixed", "Fijo"),
        ("scary", "Asustadizo"),
        ("panic", "Panico (luces en rojo)")
    )
    flicker_min_time = forms.IntegerField(
        label="Tiempo mínimo entre parpadeos")
    flicker_max_time = forms.IntegerField(
        label="Tiempo máximo entre parpadeos")
    off_on_min_time = forms.IntegerField(
        label="Tiempo mínimo entre apagones")
    off_on_max_time = forms.IntegerField(
        label="Tiempo máximo entre apagones")
    mode = forms.ChoiceField(choices=MODES_CHOICES, label="Modo")
    fixed_brightness_level = forms.IntegerField(
        label="Nivel de brillo para el modo fijo"
    )
    off_on_brightness_level = forms.IntegerField(
        label="Nivel de brillo para los apagones"
    )
