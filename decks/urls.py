from django.urls import path
from . import views

urlpatterns = [
    path('decks/', views.view_decks, name='view_decks'),
    path('decks/<int:deck_id>/', views.view_deck_detail, name='view_deck_details'),
]