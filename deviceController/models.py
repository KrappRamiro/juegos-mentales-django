from django.db import models


class Step(models.Model):
    step_name = models.CharField(max_length=140, unique=True)
    solved = models.BooleanField(default=False)


class LightConfig(models.Model):
    MODES_CHOICES = (
        ("fixed", "Modo fijo"),
        ("scary", "Modo Asustadizo"),
        ("panic", "Modo Panico (luces en rojo)"),
        ("off", "Luces apagadas")
    )
    mode = models.CharField(max_length=140, unique=True, choices=MODES_CHOICES)
    fixed_brightness = models.IntegerField()
    scary_brightness = models.IntegerField()
    uv_light_active = models.BooleanField()
    flicker_min_time = models.IntegerField()
    flicker_max_time = models.IntegerField()
    blackout_min_time = models.IntegerField()
    blackout_max_time = models.IntegerField()
