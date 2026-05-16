from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.log_in, name='log_in'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.log_out, name='log_out'),
    path('profile/', views.store, name='profile'),
    path('store/', views.store, name='store'),
    path('store/filter/', views.filter_products_ajax, name='filter_products_ajax'),
    path('about-us/', views.store, name='about'),
    path('orders/', views.my_orders, name='orders'),
    path('Get_cart_items/', views.Get_cart_items, name='Get_cart_items'),
    path('Add_to_cart/', views.Add_to_cart, name='Add_to_cart'),
    path("update_cart/", views.update_cart, name="update_cart"),
    path("remove_from_cart/", views.remove_from_cart, name="remove_from_cart"),
    path("confirm_order/", views.confirm_order, name="confirm_order"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)