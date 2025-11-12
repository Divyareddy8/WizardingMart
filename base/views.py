# base/views.py
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import Category, Product, Cart


def home(request):
    category = Category.objects.all()[:5]
    product = Product.objects.all()
    context = {'category': category, 'product': product}
    return render(request, 'base/home.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(request.GET.get('next') or 'shop')  # <— redirect to shop/cart after login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'base/login_register.html', {'page': 'login'})


def logoutUser(request):
    auth_logout(request)
    return redirect('home')

from .models import Cart


def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('shop')  # redirect to shop
        else:
            for field, errors in form.errors.items():
                for e in errors:
                    messages.error(request, f"{field}: {e}")

    return render(request, 'base/login_register.html', {'form': form, 'page': page})


def Movies(request):
    return render(request, 'base/movies.html', {})


def Shop(request):
    q = request.GET.get('q') or ''
    products = Product.objects.filter(name__icontains=q)

    if request.user.is_authenticated:
        items = Cart.objects.filter(customer=request.user, product__isnull=False)
        price = sum(item.product.price * item.quantity for item in items)
        context = {'products': products, 'items': items, 'price': price}
    else:
        context = {'products': products}

    return render(request, 'base/shop.html', context)




from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required(login_url='login')
@require_POST
def addItem(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        item, created = Cart.objects.get_or_create(product=product, customer=request.user)
        if not created:
            item.quantity += 1
        item.save()

        items = Cart.objects.filter(customer=request.user, product__isnull=False)
        total_quantity = sum(i.quantity for i in items)
        total_price = sum(i.product.price * i.quantity for i in items)

        return JsonResponse({
            'message': f'{product.name} added to cart',
            'total_quantity': total_quantity,
            'total_price': total_price
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


@login_required(login_url='login')
def myCart(request):
    items = Cart.objects.filter(customer=request.user, product__isnull=False)
    price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'base/cart.html', {'items': items, 'price': price})

@login_required(login_url='login')
@require_POST
def deleteItem(request, pk):
    try:
        item = Cart.objects.get(pk=pk, customer=request.user)
        product_name = item.product.name
        item.delete()

        items = Cart.objects.filter(customer=request.user, product__isnull=False)
        total_quantity = sum(i.quantity for i in items)
        total_price = sum(i.product.price * i.quantity for i in items)

        return JsonResponse({
            'message': f'{product_name} removed from cart',
            'total_quantity': total_quantity,
            'total_price': total_price
        })
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)



def checkout(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to checkout.")
        return redirect('login')
    items = Cart.objects.filter(customer=request.user)
    price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'base/checkout.html', {'items': items, 'price': price})

@login_required(login_url="login")
def remove(request):
    items = Cart.objects.filter(customer=request.user)
    items.delete()
    messages.success(request, "Order placed / cart cleared.")
    return redirect('shop')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Cart

