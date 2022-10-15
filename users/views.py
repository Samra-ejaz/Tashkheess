from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib import messages
User = get_user_model()


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.pop("password")
            user = User(
                **form.cleaned_data
            )
            user.set_password(password)
            user.save()
            messages.success(request, 'User Created.')
            return redirect("index")
    else:
        form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


class MyLoginView(LoginView):
    template_name = "users/login.html"


class MyLogoutView(LogoutView):
    template_name = "users/logout.html"
