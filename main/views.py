from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def show_main(request):
    return render(request, 'main.html')