from django.shortcuts import get_object_or_404, render
from .models import Deck

def view_decks(request):
    decks = Deck.objects.all().order_by('-deck_rating')
    return render(request, 'decks.html', {'decks': decks})

def view_deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    cards = deck.cards.all()

    context = {
        'deck_name': deck.deck_name,
        'deck_description': deck.deck_description,
        'deck_rating': deck.deck_rating,
        'cards': cards,
    }

    return render(request, 'deck_detail.html', context)