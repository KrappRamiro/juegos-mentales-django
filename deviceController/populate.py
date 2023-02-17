from .models import Step
solved_steps = [
    "tablero_herramientas",
    "licuadora",
    "soporte_especieros",
    "soporte_cuchillos",
    "soporte_pies",
    "teclado_heladera",
    "cuadro",
    "caldera"
]
count = Step.objects.count()
if count == 0:
    for stepname in solved_steps:
        Step.objects.create(step_name=stepname, solved=False)
