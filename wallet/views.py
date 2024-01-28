from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.cache import cache
from .models import Details
from bitcoin import *
from hdwallet import HDWallet
from hdwallet.symbols import BTC
import bs4
import requests
import qrcode
from ratelimit import limits, sleep_and_retry
import datetime

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
    user = request.user
    cached_data = cache.get(f'user_{user.id}_wallet_info')
    API_KEY = '29a1f822-ccff-4d97-840e-701f540c0276'

    @sleep_and_retry
    @limits(calls=1, period=60)
    def get_live_bitcoin_price():
        api_url = 'https://api.blockchain.com/v3/exchange/tickers/BTC-USD?apikey={API_KEY}'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                live_price = data.get('last_trade_price', 'N/A')
                print('Live BTC price fetched successfully')
                return live_price
            else:
                print(f'Error: Unable to fetch live price data. Status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None
        
    @sleep_and_retry
    @limits(calls=1, period=300)
    def get_wallet_info(address):
        api_url = f'https://blockchain.info/rawaddr/{address}?apikey={API_KEY}'
        cache_key = f'last_api_call_{address}'

        try:
            last_call_timestamp = cache.get(cache_key)
            current_timestamp = datetime.datetime.now()

            if last_call_timestamp and (current_timestamp - last_call_timestamp).seconds < 300:
                print('Insufficient time between wallet retrieval')
                messages.error(request, '*Insufficient time between wallet retrieval. Try again in a few minutes')
                return None
            
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

                cache.set(cache_key, current_timestamp)
                print('Wallet info fetched successfully')

                return {
                    'balance_satoshis': balance_satoshis,
                    'balance_btc': balance_btc,
                    'balance_usd': balance_usd,
                    'transactions': transactions,
                    'total_received': total_received,
                    'total_sent': total_sent
                }
                
            else:
                print(f'Error: Unable to fetch wallet data. Status code: {response.status_code}')
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None

    def generate_qr_code(address, output_file_path):
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(address)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        images_dir = os.path.join(static_dir, 'images')
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        output_file_path = os.path.join(images_dir, output_file_name)
        img.save(output_file_path)

    detail = Details()

    btc_address = user.first_name
    output_file_name = "qrcode.png"
    generate_qr_code(btc_address, output_file_name)

    live_btc_price = '{:,.0f}'.format(get_live_bitcoin_price())
    detail.live_btc_price = live_btc_price

    if cached_data is not None:
        detail.wallet_info = cached_data
        print('Using cached data')
    else:
        detail.wallet_info = get_wallet_info(user.first_name)
        cache.set(f'user_{user.id}_wallet_info', detail.wallet_info, timeout=3600)

    return render(request, 'dashboard.html', {'detail' : detail})

# def generate_new_address(request):
#     user = request.user
#     original_private_key = user.last_name
#     hdwallet = HDWallet(symbol=BTC)
#     wallet = hdwallet.from_private_key(original_private_key)
#     print(wallet.hdwallet.get_key())

#     return redirect('dashboard')

def refresh_wallet_info(request):
    user = request.user
    cache_key = f'user_{user.id}_wallet_info'
    cache.delete(cache_key)
    print('Cache cleared')
    return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('/')

