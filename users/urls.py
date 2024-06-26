from django.urls import path
from . import views

appname = "users"

urlpatterns = [
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('profile/<str:username>', views.profile, name='profile'),
]