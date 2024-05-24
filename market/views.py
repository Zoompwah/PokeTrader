from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Listing, Transaction, Notification
from collection.models import Collection
import ast
from django.contrib import messages

def market(request):
    query = request.GET.get('keyword', '')
    if query:
        listings = Listing.objects.filter(collection__card__name__icontains=query, is_active=True)
    else:
        listings = Listing.objects.filter(is_active=True)
    return render(request, 'market.html', {'listings': listings})

def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications.html', {'notifications': notifications, 'user': user})

def card_detail(request, collection_id):
    collection = Collection.objects.get(pk=collection_id)
    listing = Listing.objects.filter(collection=collection).order_by('-id').first()
    collection.card.types = ast.literal_eval(collection.card.types)
    collection.card.abilities = ast.literal_eval(collection.card.abilities)
    collection.card.attacks = ast.literal_eval(collection.card.attacks)
    collection.card.weaknesses = ast.literal_eval(collection.card.weaknesses)
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
        active_listings = Listing.objects.filter(is_active=True).values_list('collection_id', flat=True)
        collections = Collection.objects.filter(user=request.user).exclude(id__in=active_listings)
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
            message=f"{request.user.username} has purchased your card '{listing.collection.card.name}', email {request.user.email} to continue your transaction.",
            transaction=transaction
        )
        Notification.objects.create(
            recipient=request.user,
            message=f"You have purchased '{listing.collection.card.name}' card from {listing.seller}, email {listing.seller.email} to continue your transaction.",
            transaction=transaction
        )
        listing.is_active = False 
        listing.save()
        return redirect('market:market')
    else:
        messages.error(request, "You cannot make offer on your own card.")
        return card_detail(request, listing.collection.id)

def make_offer(request, listing_id):
    listing = Listing.objects.get(pk=listing_id, is_active=True)
    if request.user != listing.seller:
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
    else:
        messages.error(request, "You cannot make an offer on your own card.")
        return card_detail(request, listing.collection.id)
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
            message=f"Your offer of ${transaction.price} on {transaction.listing.collection.card.name} has been approved by '{transaction.seller}', email {transaction.seller.email} to continue your transaction.",
            transaction=transaction
            )
    Notification.objects.create(
            recipient=transaction.seller,
            message=f"You have approved offer of ${transaction.price} on {transaction.listing.collection.card.name}, email {transaction.buyer.email} to continue your transaction.",
            transaction=transaction
            )
    return redirect('market:notifications')

def reject_offer(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    transaction = notification.transaction
    transaction.status = 'rejected'
    transaction.save()
    listing = transaction.listing
    listing.is_active = True
    listing.save()
    Notification.objects.create(
            recipient=transaction.buyer,
            message=f"Your offer of ${transaction.price} on {transaction.listing.collection.card.name} has been rejected by '{transaction.seller}'.",
            transaction=transaction
            )
    notification.read = True
    notification.save()
    return redirect('market:notifications')

def cancel_transaction(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    transaction = notification.transaction
    transaction.status = 'cancelled'
    transaction.save()
    listing = transaction.listing
    listing.is_active = True
    listing.save()
    notification.read = True
    notification.save()
    Notification.objects.create(
            recipient=transaction.buyer,
            message=f"Your transaction on {transaction.listing.collection.card.name} has been cancelled by '{transaction.seller}'.",
            transaction=transaction
            )
    return redirect('market:notifications')

def complete_transaction(request, notification_id):
    notification = Notification.objects.get(pk=notification_id, recipient=request.user)
    transaction = notification.transaction
    transaction.status = 'completed'
    transaction.save()
    listing = transaction.listing
    listing.is_active = False
    listing.save()
    notification.read = True
    notification.save()
    collection = transaction.listing.collection
    collection.user = transaction.buyer
    collection.save()
    Notification.objects.create(
            recipient=transaction.buyer,
            message=f"Your transaction on {transaction.listing.collection.card.name} has been completed by '{transaction.seller}'.",
            transaction=transaction
            )
    return redirect('market:notifications')