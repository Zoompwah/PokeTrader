from django.db import models
from collection.models import Card
from django.conf import settings

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class Deck(models.Model):
    deck_name = models.CharField(max_length=100)
    deck_description = models.TextField()
    deck_rating = models.FloatField()
    deck_cards = models.ManyToManyField(Card)
    trader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='decks')