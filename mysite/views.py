"""Signup."""
import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.dispatch import receiver


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data.get('username')
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


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger = logging.getLogger('polls')
    logger.info(f"{user} logged in from {ip}")


@receiver(user_login_failed)
def user_logged_in_fail(sender, credentials, request, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger = logging.getLogger('polls')
    logger.warning(f"Invalid login attempt for {credentials['username']} from {ip}")