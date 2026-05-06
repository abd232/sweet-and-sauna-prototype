from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Tags, User, Customer, Product, Category, Product_category, Special_menu, Product_special_menu, discount, Product_discount, Order
from django.template.loader import render_to_string
from django.core.paginator import Paginator

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
    categories = Category.objects.all()
    tags = Tags.objects.all()

    context = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'store.html', context)


def filter_products_ajax(request):
    print(request.GET)
    products = Product.objects.all()
    search = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    selected_tags = request.GET.getlist('tags[]')
    page = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', '')

    if search:
        products = products.filter(arabic_name__icontains=search) | products.filter(name__icontains=search)

    if category_id:
        products = products.filter(categories__category__id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # If you have product-tags relation, adjust this line to your actual relation name
    if selected_tags:
        products = products.filter(tags__id__in=selected_tags).distinct()

    if sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'low_to_high':
        products = products.order_by('price')
    elif sort_by == 'high_to_low':
        products = products.order_by('-price')

    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(page)


    html = render(request, 'partials/_product_cards.html', {'products': page_obj}).content.decode('utf-8')

    return JsonResponse({
        'html': html,
        'count': products.count()
    })