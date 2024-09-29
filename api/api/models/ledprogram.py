from django.db import models

class LedProgram(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=200)

  def __init__(self, id, name): 
    self.id = id 
    self.name = name