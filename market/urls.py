from django.urls import path
from .views import card_detail,market, create_listing, notifications, purchase_card, make_offer, mark_notification_read, accept_offer, reject_offer, cancel_transaction, complete_transaction
app_name = 'market'
urlpatterns = [
    path('', market, name='market'),
    path('purchase/<int:listing_id>/', purchase_card, name='purchase_card'),
    path('offer/<int:listing_id>/', make_offer, name='make_offer'),
    path('card/<int:collection_id>/', card_detail, name='card_detail'),
    path('create_listing/', create_listing, name='create_listing'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/accept_offer/<int:notification_id>/', accept_offer, name='accept_offer'),
    path('notifications/reject_offer/<int:notification_id>/', reject_offer, name='reject_offer'),
    path('notifications/cancel_transaction/<int:notification_id>/', cancel_transaction, name='cancel_transaction'),
    path('notifications/complete_transaction/<int:notification_id>/', complete_transaction, name='complete_transaction'),
]