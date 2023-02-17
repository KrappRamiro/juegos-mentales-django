from django.db import models


class Step(models.Model):
    step_name = models.CharField(max_length=140, unique=True)
    solved = models.BooleanField(default=False)
