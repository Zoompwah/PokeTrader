from collection.models import Card, Collection
from .models import Deck, DeckCard, UserRating
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def view_decks(request):
    deck_list = Deck.objects.all().order_by('-deck_rating')
    paginator = Paginator(deck_list, 4)  # Menampilkan 4 dek per halaman
    page = request.GET.get('page')
    try:
        decks = paginator.page(page)
    except PageNotAnInteger:
        # Jika 'page' bukan integer, tampilkan halaman pertama
        decks = paginator.page(1)
    except EmptyPage:
        # Jika 'page' lebih besar dari jumlah halaman yang tersedia, tampilkan halaman terakhir
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

    # Format deck rating to display only one digit after the decimal point
    deck_rating_formatted = "{:.1f}".format(deck.deck_rating)
    cards = [c.card for c in deck_cards]

    context = {
        'deck': deck,
        'deck_rating_formatted': deck_rating_formatted,  # Add formatted rating to the context
        'cards': cards,
        'is_trader': is_trader,
    }
    return render(request, 'deck_detail.html', context)

def add_deck_rating(request, deck_id):
    if request.method == 'POST':
        deck = get_object_or_404(Deck, pk=deck_id)
        new_rating = float(request.POST.get('rating'))

        if request.user.is_anonymous:
            messages.error(request, "You must be logged in to rate a deck.")
            return redirect('view_deck_details', deck_id=deck_id)
        
        # Check if the user has already rated the deck
        if UserRating.objects.filter(user=request.user, deck=deck).exists():
            messages.error(request, "You have already rated this deck.")
            return redirect('view_deck_details', deck_id=deck_id)
        
        # Validate rating (e.g., between 0 and 5)
        if 0 <= new_rating <= 5:
            # Get all ratings for the deck
            ratings = [deck.deck_rating for deck in Deck.objects.filter(id=deck_id)]
            
            if len(ratings) == 1 and ratings[0] == 0:
                ratings = []
                
            # Add the new rating to the list
            ratings.append(new_rating)
            
            # Calculate the average rating
            average_rating = sum(ratings) / len(ratings)
            
            # Update the deck's rating
            deck.deck_rating = average_rating
            deck.save()
            
            # Save the user's rating to prevent them from rating again
            UserRating.objects.create(user=request.user, deck=deck, rating=new_rating)

            messages.success(request, 'Rate successful!')
            
            return redirect('view_deck_details', deck_id=deck_id)
        else:
            messages.error(request, "Invalid rating. Please enter a rating between 0 and 5.")
    
    # If not a POST request or invalid rating, or user not logged in, redirect to deck detail
    return redirect('view_deck_details', deck_id=deck_id)

@login_required
def create_deck(request):
    if request.method == 'POST':
        deck_name = request.POST['deck_name']
        deck_description = request.POST['deck_description']
        deck_card = request.POST.getlist('deck_cards')

        print("deck_card")
        print(deck_card)

        # Assuming the trader is the currently logged-in user
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
    
    # Check if the deck belongs to the current user
    if deck.trader != request.user:
        messages.error(request, "You are not authorized to delete this deck.")
        return redirect('view_deck_details', deck_id=deck.pk)

    if request.method == 'POST':
        # Delete associated DeckCard objects
        deck.deckcard_set.all().delete()
        
        # Delete the deck itself
        deck.delete()

        messages.success(request, "Deck deleted successfully.")
        return redirect('/decks')  # Redirect to the home page or any other appropriate page after deletion

    return render(request, 'deck_delete.html', {'deck': deck})
