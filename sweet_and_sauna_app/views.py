from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Tags, User, Customer, Product, Category, Product_category, Special_menu, Product_special_menu, discount, Product_discount, Order


def index(request):
    special_menus = Special_menu.objects.all().order_by('priority')
    context = {
        'special_menus': special_menus,
    }
    return render(request, 'index.html', context)

def log_in(request):
    if request.method == 'POST':
        errors = Customer.objects.validate_login(request.POST)
        if errors:
            context={
                'errors' : errors,
            }
            return render(request , 'account/log_in.html' , context=context)
        else:
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.filter(email=email).first()
            if user is not None:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
    return render(request, 'account/log_in.html')

def register(request):
    if request.method == 'POST':
        errors = Customer.objects.validate_registration(request.POST)
        if errors:
            context={
                'errors' : errors,
            }
            return render(request , 'account/log_in.html' , context=context)
        else:
            Customer.objects.create_customer(request.POST)
            return redirect('/accounts/login/')
    return render(request, 'account/log_in.html')

def log_out(request):
    logout(request)

    return redirect('/') 

def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    tags = Tags.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'store.html', context)