"""Signup."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = form.save()
            login(request, user, raw_passwd)
            return redirect('polls:index')
        else:
            # what if form is not valid?
            # we should display a message in signup.html
            messages.error(request, "We can't signup to make your accounts.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
