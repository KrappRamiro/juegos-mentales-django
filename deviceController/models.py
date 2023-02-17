from django.db import models


class Step(models.Model):
    step_name = models.CharField(max_length=150, unique=True)
    solved = models.BooleanField(default=False)
