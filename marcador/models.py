from django.db import models

class Vokabel(models.Model):
	norwegisch = models.CharField(max_length=150)
	deutsch = models.CharField(max_length=150)
	kapitel = models.IntegerField()