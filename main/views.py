from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here
def homepage(request):
    return render(request, 'main.html')