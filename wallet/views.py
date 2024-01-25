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
        
    

    if request.method == 'POST':
        addr = request.POST['addr']
        # res2 = requests.get('https://cryptowat.ch/')
        # soup2 = bs4.BeautifulSoup(res2.text, 'lxml')
        # live_price = soup2.find_all('span', {'class': 'price'})
        # live_bitcoin_price = live_price[1].getText()
        # live_bitcoin_price1 = live_price[1].getText()
        live_btc_price = get_live_bitcoin_price()
        print(live_btc_price)

        # res = requests.get('https://www.blockchain.com/explorer/addresses/btc/'+ addr)
        
        # if res:
            # soup = bs4.BeautifulSoup(res.text, 'lxml')
            # print('soup is', soup)
            # bal = soup.find_all('span', {'class': 'sc-5f049527-7 Prcrh'})
            # print('balance is', bal)
            # bal[4].getText()
            # final_bal = bal[4].getText()
            # final_bal1 = final_bal.replace(" ", "").rstrip()[:-3].upper()
            # transactions = bal[1].getText()
            # total_received = bal[2].getText()
            # total_received1 = total_received.replace(" ", "").rstrip()[:-3].upper()
            # total_sent = bal[3].getText()
            # total_sent1 = total_sent.replace(" ", "").rstrip()[:-3].upper()
            # final_bal1_int = float(final_bal1)
            # total_received1_int = float(total_received1)
            # total_sent1_int = float(total_sent1)
            # live_bitcoin_price1_int = float(live_bitcoin_price1)
            
            # balance_usd = final_bal1_int*live_bitcoin_price1_int
            # total_received_usd = total_received1_int*live_bitcoin_price1_int
            # total_sent_usd = total_sent1_int*live_bitcoin_price1_int
        # else:
            # return redirect('/')

        detail = Details()
        # detail.balance = final_bal
        # detail.balance1 = final_bal1
        # detail.transactions = transactions
        # detail.total_received = total_received
        # detail.total_received1 = total_received1
        # detail.total_sent = total_sent
        # detail.total_sent1 = total_sent1
        detail.live_btc_price = live_btc_price
        # detail.live_bitcoin_price1 = live_bitcoin_price1
        # detail.balance_usd = int(balance_usd)
        # detail.total_received_usd = int(total_received_usd)
        # detail.total_sent_usd = int(total_sent_usd)


    else:
        detail = '   '

    return render(request, 'index.html', {'detail' : detail})
    # return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
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
                return redirect('/')

        else:
            messages.error(request, 'Passwords not matching.')
            return redirect('register')
        
    else:
        return render(request, 'register.html', {'detail': detail})

def logout(request):
    auth.logout(request)
    return redirect('/')