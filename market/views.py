from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Listing, Transaction, Notification
from collection.models import Card
from .forms import ListingForm

def market(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, 'market.html', {'listings': listings})

def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

def card_detail(request, card_id):
    card = Card.objects.get(pk=card_id)
    return render(request, 'card_detail.html', {'card': card})

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, user=request.user)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('market')
    else:
        form = ListingForm(user=request.user)
    return render(request, 'create_listing.html', {'form': form})


def purchase_card(request, listing_id):
    listing = Listing.objects.get(pk=listing_id, is_active=True)
    if request.user != listing.seller:
        transaction = Transaction.objects.create(
            listing=listing,
            buyer=request.user,
            seller=listing.seller,
            price=listing.price,
            status='pending'
        )
        Notification.objects.create(
            recipient=listing.seller,
            message=f"{request.user.username} has purchased your card '{listing.card.name}'.",
            transaction=transaction
        )
        listing.is_active = False 
        listing.save()
        return redirect('transaction_history')
    return redirect('market')

def make_offer(request, listing_id):
    listing = Listing.objects.get(pk=listing_id, is_active=True)
    if request.method == 'POST':
        offer_price = request.POST.get('offer_price')
        if request.user != listing.seller:
            transaction = Transaction.objects.create(
                listing=listing,
                buyer=request.user,
                seller=listing.seller,
                price=offer_price,
                status='offer_made',
                offer_made=True
            )
            Notification.objects.create(
            recipient=listing.seller,
            message=f"{request.user.username} has made an offer of ${offer_price} on your card '{listing.card.name}'.",
            transaction=transaction
            )
            return redirect('market')
    return render(request, 'card_detail.html', {'listing': listing})

def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return redirect(request.GET.get('next', 'market:market'))

def accept_offer(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    transaction = notification.transaction
    transaction.status = 'accepted'
    transaction.save()
    notification.read = True
    notification.save()
    return redirect('notifications')

def reject_offer(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    transaction = notification.transaction
    transaction.status = 'rejected'
    transaction.save()
    notification.read = True
    notification.save()
    return redirect('notifications')