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
                auth.login(request, user)
                messages.success(request, 'User Created')
                return redirect('dashboard')

        else:
            messages.error(request, 'Passwords not matching.')
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'detail': detail})

def dashboard(request):
    def get_live_bitcoin_price():
        api_url = 'https://api.blockchain.com/v3/exchange/tickers/BTC-USD'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                live_price = data.get('last_trade_price', 'N/A')
                return live_price
            else:
                print(f'Error: Unable to fetch data. Status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None
        
    def get_wallet_info(address):
        api_url = f'https://blockchain.info/rawaddr/{address}'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                balance_satoshis = data.get('final_balance', 'N/A')
                balance_btc = '{:.9f}'.format(balance_satoshis / 100000000)
                usd = float('{:.5f}'.format(balance_satoshis / 100000000)) * get_live_bitcoin_price()
                balance_usd = '{:.2f}'.format(usd)
                transactions = data.get('n_tx', 'N/A')
                total_received = data.get('total_received', 'N/A')
                total_sent = data.get('total_sent', 'N/A')
                print(balance_usd)

                return {
                    'balance_satoshis': balance_satoshis,
                    'balance_btc': balance_btc,
                    'balance_usd': balance_usd,
                    'transactions': transactions,
                    'total_received': total_received,
                    'total_sent': total_sent
                }

            else:
                print(f'Error: Unable to fetch data. Status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None


    detail = Details()
    user = request.user
    live_btc_price = get_live_bitcoin_price()
    

    if live_btc_price is not None:
        detail.live_btc_price = live_btc_price
    else:
        detail.live_btc_price = 'N/A'

    wallet_info = get_wallet_info(user.first_name)
    detail.wallet_info = wallet_info

    return render(request, 'dashboard.html', {'detail' : detail})

def logout(request):
    auth.logout(request)
    return redirect('/')

