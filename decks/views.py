from django.shortcuts import render
from .models import Deck

def view_decks(request):
    decks = Deck.objects.all().order_by('-deck_rating')
    return render(request, 'decks.html', {'decks': decks})