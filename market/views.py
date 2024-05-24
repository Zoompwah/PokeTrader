from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Listing, Transaction, Notification
from collection.models import Collection

def market(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, 'market.html', {'listings': listings})

def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})

def card_detail(request, collection_id):
    collection = Collection.objects.get(pk=collection_id)
    listing = Listing.objects.get(collection=collection)
    return render(request, 'card_detail.html', {'collection': collection, 'listing': listing})

def create_listing(request):
    if request.method == 'POST':
        collection = request.POST.get('collection')
        price = request.POST.get('price')
        seller = request.user
        new_listing = Listing.objects.create(
            collection=Collection.objects.get(pk=collection),
            price=price,
            seller=seller
        )
        new_listing.save()
        return redirect('market:market')
    else:
        collections = Collection.objects.filter(user=request.user)
    return render(request, 'add_listing.html', {'collections': collections})


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
            message=f"{request.user.username} has purchased your card '{listing.collection.card.name}'.",
            transaction=transaction
        )
        listing.is_active = False 
        listing.save()
        return redirect('market:market')
    return redirect('market:market')

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
            message=f"{request.user.username} has made an offer of ${offer_price} on your card '{listing.collection.card.name}'.",
            transaction=transaction
            )
            return redirect('market:market')
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
    listing = transaction.listing
    listing.is_active = False
    listing.save()
    notification.read = True
    notification.save()
    Notification.objects.create(
            recipient=transaction.buyer,
            message=f"Your offer of ${transaction.price} on {transaction.listing.collection.card.name} has been approved by '{transaction.seller}'.",
            transaction=transaction
            )
    return redirect('market:notifications')

def reject_offer(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    transaction = notification.transaction
    transaction.status = 'rejected'
    transaction.save()
    notification.read = True
    notification.save()
    return redirect('market:notifications')