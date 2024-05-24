from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm



# Create your views here.

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')

    else:
        form = UserRegistrationForm()

    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("/")

    form = UserLoginForm()

    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
        )

@login_required
def custom_logout(request):
    logout(request)
    return HttpResponseRedirect('login')

def profile(request, username):
    if request.method == "POST":
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()
            return redirect("profile", user_form.username)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(
            request=request,
            template_name="profile.html",
            context={"form": form}
            )
    
    return redirect("homepage")
