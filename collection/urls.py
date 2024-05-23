from django.urls import path
from collection.views import add_cards_to_collection, remove_cards_from_collection, view_collection

app_name = 'collection'
urlpatterns = [
    path('', view_collection),
    path('add', add_cards_to_collection),
    path('remove/<int:card_id>', remove_cards_from_collection),
]
