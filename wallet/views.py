from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Details
from bitcoin import *
import bs4
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

def register(request):
    detail = Details()
    private_key = random_key()
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    detail.private_key = private_key
    detail.public_key = public_key
    detail.address = address


    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        private_key = request.POST['private_key']
        public_key = request.POST['public_key']
        address = request.POST['address']

        if not username or not email or not password or not password2:
            messages.error(request, 'All fields are required.')
            return redirect('register')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return redirect('register')

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email taken.')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, last_name=private_key, first_name=address)
                user.save();
                messages.success(request, 'User Created')
                return redirect('dashboard')

        else:
            messages.error(request, 'Passwords not matching.')
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'detail': detail})


def dashboard(request):
    return render(request, 'dashboard.html')