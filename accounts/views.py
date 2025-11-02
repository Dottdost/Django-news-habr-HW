from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'USER'
            user.save()
            messages.success(request, 'Registration successful! Log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Hello, {user.username}! Glad to see you again")
            return redirect('home')

        if user is not None:
            if user.is_banned:
                messages.error(request, 'Your account has been blocked.')
                return redirect('login')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')
