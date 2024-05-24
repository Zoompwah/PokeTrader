from collection.models import Card, Collection
from .models import Deck, DeckCard, UserRating
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def view_decks(request):
    deck_list = Deck.objects.all().order_by('-deck_rating')
    paginator = Paginator(deck_list, 4)
    page = request.GET.get('page')
    try:
        decks = paginator.page(page)
    except PageNotAnInteger:
        decks = paginator.page(1)
    except EmptyPage:
        decks = paginator.page(paginator.num_pages)
    
    for deck in decks:
        deck.deck_rating = "{:.1f}".format(deck.deck_rating)
    return render(request, 'decks.html', {'decks': decks})


def view_deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    deck_cards = DeckCard.objects.filter(deck=deck)
    is_trader = False

    if request.user == deck.trader:
        is_trader = True

    print(is_trader)

    deck_rating_formatted = "{:.1f}".format(deck.deck_rating)
    cards = [c.card for c in deck_cards]

    context = {
        'deck': deck,
        'deck_rating_formatted': deck_rating_formatted,
        'cards': cards,
        'is_trader': is_trader,
    }
    return render(request, 'deck_detail.html', context)

def add_deck_rating(request, deck_id):
    if request.method == 'POST':
        deck = get_object_or_404(Deck, pk=deck_id)
        new_rating = request.POST.get('rating')

        if request.user.is_anonymous:
            messages.error(request, "You must be logged in to rate a deck.")
            return redirect('view_deck_details', deck_id=deck_id)
    
        if UserRating.objects.filter(user=request.user, deck=deck).exists():
            messages.error(request, "You have already rated this deck.")
            return redirect('view_deck_details', deck_id=deck_id)
        
        if new_rating == "":
            new_rating = 0
            messages.error(request, "Invalid rating. Please enter a rating between 0 and 5.")
            return redirect('view_deck_details', deck_id=deck_id)
        
        new_rating = float(new_rating)
        if 0 <= new_rating <= 5:
            
            ratings = [deck.deck_rating for deck in Deck.objects.filter(id=deck_id)]
            
            if len(ratings) == 1 and ratings[0] == 0:
                ratings = []
            ratings.append(new_rating)
            average_rating = sum(ratings) / len(ratings)
            deck.deck_rating = average_rating
            deck.save()
            
            UserRating.objects.create(user=request.user, deck=deck, rating=new_rating)
            messages.success(request, 'Rate successful!')
            return redirect('view_deck_details', deck_id=deck_id)
        else:
            messages.error(request, "Invalid rating. Please enter a rating between 0 and 5.")
    
    return redirect('view_deck_details', deck_id=deck_id)

@login_required
def create_deck(request):
    if request.method == 'POST':
        deck_name = request.POST['deck_name']
        deck_description = request.POST['deck_description']
        deck_card = request.POST.getlist('deck_cards')

        print("deck_card")
        print(deck_card)

        trader = request.user

        deck = Deck(
            deck_name=deck_name,
            deck_description=deck_description,
            deck_rating=0,
            trader=trader
        )
        deck.save()

        for card_id in deck_card:
            card = Card.objects.get(id=int(card_id))
            deck_card = DeckCard(deck=deck, card=card)
            deck_card.save()

        return redirect('view_deck_details', deck_id=deck.pk)

    return render(request, 'create_deck.html', {'cards' : [c.card for c in Collection.objects.filter(user=request.user.id)]})

@login_required
def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    
    if deck.trader != request.user:
        messages.error(request, "You are not authorized to delete this deck.")
        return redirect('view_deck_details', deck_id=deck.pk)

    if request.method == 'POST':
        deck.deckcard_set.all().delete()
        deck.delete()

        messages.success(request, "Deck deleted successfully.")
        return redirect('/decks')

    return render(request, 'deck_delete.html', {'deck': deck})

@login_required
def edit_deck(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    if deck.trader != request.user:
        messages.error(request, "You are not authorized to edit this deck.")
        return redirect('view_deck_details', deck_id=deck.pk)

    if request.method == 'POST':
        deck_name = request.POST['deck_name']
        deck_description = request.POST['deck_description']
        deck_cards = request.POST.getlist('deck_cards')

        # Update deck details
        deck.deck_name = deck_name
        deck.deck_description = deck_description

        # Clear existing cards in the deck
        deck.deckcard_set.all().delete()

        # Add new cards to the deck
        for card_id in deck_cards:
            card = Card.objects.get(id=int(card_id))
            deck_card = DeckCard(deck=deck, card=card)
            deck_card.save()

        deck.save()
        messages.success(request, "Deck updated successfully.")
        return redirect('view_deck_details', deck_id=deck.pk)

    return render(request, 'edit_deck.html', {'deck': deck, 'cards': [c.card for c in Collection.objects.filter(user=request.user.id)]})
