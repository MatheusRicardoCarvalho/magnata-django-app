from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from wallet.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import F

@login_required
def wallet(request):
    wallets = Wallet.objects.filter(user=request.user)
    context = {'wallets': wallets}
    return render(request, 'wallet/home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def wallet_management(request):
    wallet_id = request.GET.get('wallet_id')
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    print('Minha carteira', wallet)
    stocks = StockInWallet.objects.filter(wallet=wallet)
    print('Minhas acoes', stocks)

    context = {'wallet': wallet, 'stocks': stocks}
    return render(request, 'wallet/wallet_management.html', context)

@login_required
def buy_stock(request):
    if(request.method == 'POST'):
        wallet_id = request.POST.get('wallet_id')
        stock_id = request.POST.get('stock_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        date = request.POST.get('date')

        wallet = Wallet.objects.get(id=wallet_id)
        stock = Stock.objects.get(id=stock_id)

        try:
            stock_in_wallet = StockInWallet.objects.get(wallet=wallet, stock=stock)

            stock_in_wallet.total = F('total') + quantity
            stock_in_wallet.save()
        except StockInWallet.DoesNotExist:
            stock_in_wallet = StockInWallet.objects.create(
                wallet=wallet,
                stock=stock,
                total=quantity
            )

        buy_stock = BuyHistory.objects.create(
            wallet=wallet,
            stock_in_wallet=stock_in_wallet,
            price=price,
            quantity=quantity,
            date=date
        )
        context = {'wallet': wallet, 'stocks': StockInWallet.objects.filter(wallet=wallet)}
        return render(request,'wallet/wallet_management.html', context=context)
    
    wallet_id = request.GET.get('wallet_id')
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    print('Minha carteira', wallet)
    print('Tipo da carteira', wallet.type)
    if wallet.type == "Brasileira":
        print('walletType', WalletType)
        available_stocks = Stock.objects.exclude(classification__name__in=WalletType)
    else:
        available_stocks = Stock.objects.filter(classification__name=wallet.type)
    context = {'available_stocks': available_stocks, 'wallet_id': wallet_id}
    return render(request, 'wallet/buy_stock.html', context=context)

def add_wallet(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        name = request.POST.get('name')
        description = request.POST.get('description')

        wallet = Wallet.objects.create(user_id=user, name=name, description=description)

        return redirect('wallet_list')

    return render(request, 'wallet_form.html')

@login_required
def create_wallet(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        description = request.POST.get('description')
        type = request.POST.get('type')

        wallet = Wallet.objects.create(user=user, name=name, description=description, type=type)

        return redirect('home')
    
    context = {"WalletType": WalletType}
    return render(request, 'wallet/create_wallet.html', context=context)

@login_required
def home(request):
    wallets = Wallet.objects.filter(user=request.user)
    context = {'wallets': wallets}
    return render(request, 'wallet/home.html', context)

@login_required
def add_stock(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ticker = request.POST.get('ticker')

        new_classification_name = request.POST.get('new_classification')
        if new_classification_name:
            classification, created = Classification.objects.get_or_create(name=new_classification_name)
        else:
            classification_id = request.POST.get('classification')
            classification = Classification.objects.get(id=classification_id)

        new_sector_name = request.POST.get('new_sector')
        if new_sector_name:
            sector, created = Sector.objects.get_or_create(name=new_sector_name)
        else:
            sector_id = request.POST.get('sector')
            sector = Sector.objects.get(id=sector_id)

        Stock.objects.create(name=name, ticker=ticker, classification=classification, sector=sector)

        return redirect('home')
    if (not request.user.is_superuser):
        return redirect('home')
    classifications = Classification.objects.all()
    sectors = Sector.objects.all()
    context = {'classifications': classifications, 'sectors': sectors}
    return render(request, 'wallet/add_stock.html', context)

@login_required
def sell_stock(request):
    if request.method == 'POST':
        print('Vendendo ação')
        stock_in_wallet_id = request.POST.get('stock_in_wallet_id')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        date = request.POST.get('date')
        wallet_id = request.POST.get('wallet_id')

        stock_in_wallet = get_object_or_404(StockInWallet, id=stock_in_wallet_id)
        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)

        if stock_in_wallet.total >= quantity:
            SellHistory.objects.create(
                wallet=wallet,
                stock_in_wallet=stock_in_wallet,
                price=price,
                quantity=quantity,
                date=date
            )

            stock_in_wallet.total -= quantity
            stock_in_wallet.save()

            if stock_in_wallet.total == 0:
                stock_in_wallet.delete()

        return redirect(f'/wallet/wallet_management?wallet_id={wallet_id}')

@login_required
def delete_wallet(request):
    if request.method == 'POST':
        wallet_id = request.POST.get('wallet_id')
        wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
        wallet.delete()
        return redirect('home')
    return redirect('home')