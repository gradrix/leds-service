from __future__ import unicode_literals
from django.db import models

class ModeLayout(models.Model):

  modeId = models.IntegerField(primary_key=True)
  modes = []
  minSpeed = models.IntegerField()
  maxSpeed = models.IntegerField()
  service = models.IntegerField()