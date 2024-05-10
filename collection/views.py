from django.http import HttpResponseRedirect
from django.urls import reverse
from collection.models import Card, Collection
from django.shortcuts import render

# Create your views here.
def view_collection(request):
    collection = Card.objects.filter(user=request.user)
    context = {'collection': collection}

    return render(request, "collections.html", context)

def add_cards_to_collection(request, cards_name):
    if request.method == 'POST':
        for card_name in cards_name:
            Collection.objects.create(
                user = request.user,
                card = Card.objects.get(name=card_name)
            )

        return HttpResponseRedirect(reverse('collection:view_collection'))

    context = {'owned_cards': Collection.objects.filter(user=request.user)}

    return render(request, "add_cards.html", context)
    
def remove_cards_from_collection(request, card_name):
    if request.method == 'POST':
        Collection.objects.get(name=card_name).delete()

        return HttpResponseRedirect(reverse('collection:view_collection'))
