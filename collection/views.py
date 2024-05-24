from django.http import HttpResponseRedirect
from django.urls import reverse
from collection.models import Card, Collection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def view_collection(request):
    collection = Collection.objects.filter(user=request.user)
    context = {'collection': [c.card for c in collection]}

    return render(request, "collections.html", context)

@login_required
def add_cards_to_collection(request):
    if request.method == 'POST':
        cards_id = request.POST.getlist('cards')
        for card_id in cards_id:
            card = Card.objects.get(id=int(card_id))
            Collection.objects.get_or_create(user=request.user, card=card)

        return HttpResponseRedirect("/collection/")

    context = {'owned_cards': [c.card for c in Collection.objects.filter(user=request.user.id)], 'all_cards': Card.objects.all()}

    return render(request, "add_cards.html", context)
    
@login_required
def remove_cards_from_collection(request, card_id):
    if request.method == 'POST':
        try:
            Collection.objects.get(card=Card.objects.get(id=int(card_id)), user=request.user.id).delete()
        except:
            pass

        return HttpResponseRedirect("/collection/")
