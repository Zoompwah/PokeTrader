from collection.models import Card
from django.shortcuts import render

# Create your views here.
def view_collection(request):
    collection = Card.objects.filter(user=request.user)
    context = {'collection': collection}

    return render(request, "", context)

def add_cards_to_collection(request):
    pass
    
def remove_cards_from_collection(request):
    pass
