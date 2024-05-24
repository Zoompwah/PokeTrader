from .models import Deck
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

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

@login_required
def add_rating(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    new_rating = float(request.POST['rating'])
    deck.deck_rating = (deck.deck_rating + new_rating) / 2
    deck.save()

    return render(request, 'deck_detail.html', {'deck': deck})