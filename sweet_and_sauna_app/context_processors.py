from django.db.models import Sum
from .models import CartItem


def cart_counter(request):
    cart_count = None

    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()

    return {
        "cart_count": cart_count
    }