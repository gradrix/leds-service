from __future__ import unicode_literals
from django.db import models

class LedSettings (models.Model):
    host = models.IntegerField()
    isOn = models.BooleanField()
    brightness = models.IntegerField()
    mode = models.IntegerField()
    toggle = models.IntegerField()
    speed = models.IntegerField()
    service = models.IntegerField()
