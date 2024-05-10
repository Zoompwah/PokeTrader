from django.db import models
from django.contrib.auth.models import User
from collection.models import Card  

class Listing(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)

class Transaction(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sales', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    offer_made = models.BooleanField(default=False)

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    transaction = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - Read: {self.read}"