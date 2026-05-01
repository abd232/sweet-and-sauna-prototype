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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)