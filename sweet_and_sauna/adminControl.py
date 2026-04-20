from django.contrib import admin

from sweet_and_sauna_app.models import Category, Customer, Order, Product, Product_category, Product_discount, Product_special_menu, Product_tag, Special_menu, Tags, discount

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Product_category)
admin.site.register(Special_menu)
admin.site.register(Product_special_menu)
admin.site.register(discount)
admin.site.register(Product_discount)
admin.site.register(Order)          
admin.site.site_header = "Sweet & Sauna Admin"
admin.site.site_title = "Sweet & Sauna Admin Portal"
admin.site.index_title = "Welcome to Sweet & Sauna Admin Portal"
admin.site.register(Tags)
admin.site.register(Product_tag)

def removeAdmins(request):
    from django.contrib.auth.models import User
    User.objects.filter(is_superuser=True).delete()
    
