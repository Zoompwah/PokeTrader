from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_decks, name='view_decks'),
    path('<int:deck_id>/', views.view_deck_detail, name='view_deck_details'),
    path('<int:deck_id>/add_rating/', views.add_deck_rating, name='add_deck_rating'),
    path('create/', views.create_deck, name='create_deck'),
    path('<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),
    path('<int:deck_id>/edit/', views.edit_deck, name='edit_deck'),
]