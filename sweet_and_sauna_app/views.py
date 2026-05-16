from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.db import transaction
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from .models import Tags, User, Customer, Product, Category, Product_category, Special_menu, Product_special_menu, discount, Product_discount, Order, CartItem, OrderItem
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from decimal import Decimal

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

def my_orders(request):
    orders_list = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    paginator = Paginator(orders_list, 2)
    page_number = request.GET.get("page")
    orders = paginator.get_page(page_number)

    return render(request, "orders.html", {
        "orders": orders
    })

def make_order(request):
    if request.method == "POST":
        # Handle order creation logic here
        pass
    return Http404("Product not found")

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

def Get_cart_items(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "authenticated": False,
            "items": [],
            "total": "0.00"
        })

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related("product")
    )

    items = []
    total = Decimal("0.00")

    for item in cart_items:
        item_total = item.price * item.quantity
        total += item_total

        items.append({
            "id": item.id,
            "product_id": item.product.id,
            "name": item.product.arabic_name,
            "image": item.product.image.url if item.product.image else "",
            "price": str(item.price),
            "quantity": item.quantity,
            "item_total": str(item_total),
        })

    return JsonResponse({
        "authenticated": True,
        "items": items,
        "total": str(total)
    })

def Add_to_cart(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "Invalid request method"},
            status=405
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "يجب تسجيل الدخول أولاً"},
            status=401
        )

    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity", 1))

    if quantity < 1:
        quantity = 1

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={
            "price": product.price,
            "quantity": quantity
        }
    )

    # If product already exists in cart, add the new quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.price = product.price
        cart_item.save()

    cart_count = (
        CartItem.objects
        .filter(user=request.user)
        .aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    cart_count_display = "5+" if cart_count > 5 else str(cart_count)

    return JsonResponse({
        "success": True,
        "message": "تمت إضافة المنتج إلى السلة",
        "cart_item_id": cart_item.id,
        "cart_count": cart_count,
        "cart_count_display": cart_count_display
    })

def update_cart(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request method"
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": "You must be logged in"
        }, status=401)

    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity", 1)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return JsonResponse({
            "success": False,
            "error": "Invalid quantity"
        }, status=400)

    if quantity < 1:
        quantity = 0

    cart_item = CartItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).first()

    if not cart_item:
        return JsonResponse({
            "success": False,
            "error": "Item not found"
        }, status=404)
    if(quantity == 0):
        cart_item.delete()
        cart_total = sum(
            item.price * item.quantity
            for item in CartItem.objects.filter(user=request.user)
        )
        cart_count = (
            CartItem.objects
            .filter(user=request.user)
            .aggregate(total=Sum("quantity"))["total"]
            or 0
        )
        cart_count_display = "5+" if cart_count > 5 else str(cart_count)

        return JsonResponse({
            "success": True,
            "quantity": 0,
            "item_total": "0.00",
            "cart_total": str(cart_total),
            "cart_count_display": cart_count_display,
        })
    cart_item.quantity = quantity
    cart_item.save()

    item_total = cart_item.price * cart_item.quantity

    cart_total = sum(
        item.price * item.quantity
        for item in CartItem.objects.filter(user=request.user)
    )

    cart_count = (
        CartItem.objects
        .filter(user=request.user)
        .aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    cart_count_display = "5+" if cart_count > 5 else str(cart_count)

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity,
        "item_total": str(item_total),
        "cart_total": str(cart_total),
        "cart_count_display": cart_count_display,
    })

def remove_from_cart(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request method"
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": "You must be logged in"
        }, status=401)

    product_id = request.POST.get("product_id")

    cart_item = CartItem.objects.filter(
        user=request.user,
        product_id=product_id
    ).first()

    if not cart_item:
        return JsonResponse({
            "success": False,
            "error": "Item not found"
        }, status=404)

    cart_item.delete()

    cart_total = sum(
        item.price * item.quantity
        for item in CartItem.objects.filter(user=request.user)
    )

    cart_count = (
        CartItem.objects
        .filter(user=request.user)
        .aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    cart_count_display = "5+" if cart_count > 5 else str(cart_count)

    return JsonResponse({
        "success": True,
        "cart_total": str(cart_total),
        "cart_count": cart_count,
        "cart_count_display": cart_count_display
    })

def confirm_order(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request method"
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": "يجب تسجيل الدخول أولاً"
        }, status=401)

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related("product")
    )

    if not cart_items.exists():
        return JsonResponse({
            "success": False,
            "error": "سلة التسوق فارغة"
        }, status=400)

    total = Decimal("0.00")

    for item in cart_items:
        total += item.price * item.quantity

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            total=total,
            status="pending"
        )

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
            for item in cart_items
        ]

        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()

    return JsonResponse({
        "success": True,
        "message": "تم تأكيد طلبك بنجاح",
        "order_id": order.id
    })