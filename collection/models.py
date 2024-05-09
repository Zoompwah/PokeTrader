from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=100)
    card_image = models.CharField(max_length=100)
    types = models.CharField(max_length=100)
    abilities = models.CharField(max_length=100)
    attacks = models.CharField(max_length=100)
    weaknesses = models.CharField(max_length=100)
