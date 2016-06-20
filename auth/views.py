from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from .forms import LoginForm, CreateUserForm, ChangePasswordForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)

            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.add_message(request, messages.WARNING, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'User Created.')
            return redirect('index')
    else:
        form = CreateUserForm()
    return render(request, 'auth/create_user.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['old_password']
            user = request.user
            if user.check_password(password):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Your password has been updated.')
                return redirect('index')
            else:
                messages.add_message(request, messages.WARNING, 'Invalid password.')
    else:
        form = ChangePasswordForm()
    return render(request, 'auth/change_password.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.WARNING, 'You have been logged out.')
    request.session.flush()
    return redirect('login')
