from django.db import models
from django.contrib.auth.models import User
from PokeTrader.collection.models import Card

class Deck(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cards = models.ManyToManyField(Card, related_name='decks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name