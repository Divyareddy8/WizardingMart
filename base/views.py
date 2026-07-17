from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    category = Category.objects.all()[0:5]
    product = Product.objects.all()

    context = {'category': category, 'product': product}
    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    return render(request, 'base/login_register.html', {'form': form})

def Movies(request):
    return render(request, 'base/movies.html', {})

def Shop(request):
    q = request.GET.get('q') if request.GET.get('q') != None else  ''
    products = Product.objects.filter(name__icontains=q)
    if request.user.is_authenticated:
        items = Cart.objects.filter(customer = request.user)
        price = sum(item.product.price * item.quantity for item in items)
        context = {'products': products, 'items': items, 'price': price}
    else:
        context = {'products': products}
    return render(request, 'base/shop.html', context)

def myCart(request): 
    return render(request, 'base/cart.html')

@login_required(login_url = "login")
def addItem(request, pk):
    product = Product.objects.get(id = pk)
    item, created = Cart.objects.get_or_create(product = product, customer = request.user)
    item.quantity += 1
    item.save()
    return redirect('shop')

@login_required(login_url = "login")
def deleteItem(request, pk):
    item = Cart.objects.get(id = pk)
    item.delete()
    return redirect('shop')

def checkout(request):
    return render(request, 'base/checkout.html')

def remove(request):
    items = Cart.objects.filter(customer = request.user)
    items.delete()
    return redirect('shop')