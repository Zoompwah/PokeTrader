from django.db import models
from collection.models import Card
from django.conf import settings

class Deck(models.Model):
    deck_name = models.CharField(max_length=100)
    deck_description = models.TextField()
    deck_rating = models.FloatField()
    trader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

class UserRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    rating = models.FloatField()

    class Meta:
        unique_together = ('user', 'deck')