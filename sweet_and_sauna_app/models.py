import bcrypt
from django.contrib.auth.models import User
from django.db import models

class CustomerManger(models.Manager):
    def create_customer(self,post_data):
        user = User.objects.create_user(username=post_data['email'], email=post_data['email'], password=post_data['password'])
        customer = Customer.objects.create(user=user, phone=post_data['phone'], address=post_data['address'])
        return customer
    
    def validate_login(self,post_data):
        errors={}
        email = post_data.get('email' , '')
        password = post_data.get('password' , '')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                errors['user'] = 'Email or password not valid'
        else:
            errors['user'] = 'Email or password not valid'
        return errors
    def validate_registration(self,post_data):
        errors={}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if len(post_data['email']) < 5:
            errors['email'] = 'Email must be at least 5 characters long'
        if User.objects.filter(email=post_data['email']).exists():
            errors['email'] = 'Email already exists'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'
        if post_data['phone'] and len(post_data['phone']) < 4:
            errors['phone'] = 'Phone number must be at least 4 characters long'
        if post_data['address'] and len(post_data['address']) < 10:
            errors['address'] = 'Address must be at least 10 characters long'
        return errors
    
class CartManger(models.Manager):
    def create_cart_item(self, user, product, price, quantity):
        cart_item = CartItem.objects.filter(user=user, product=product).first()
        if not cart_item:
            CartItem.objects.create(user=user, product=product, price=price, quantity=quantity)
        else:
            cart_item.quantity += quantity
            cart_item.save()
        return True
    def update_cart_item(self, user, product, price, quantity): 
        cart_item = CartItem.objects.filter(user=user, product=product).first()
        if cart_item:
            cart_item.price = price
            cart_item.quantity = quantity
            cart_item.save()
            return True
        return False
    def remove_cart_item(self, user, product):
        cart_item = CartItem.objects.filter(user=user, product=product).first()
        if cart_item:
            cart_item.delete()
            return True
        return False

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    Updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManger()

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=100)
    arabic_name = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(null=True,upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    arabic_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product_category(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.category.name}"
        

class Special_menu(models.Model):
    PRIORITY_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]
    name = models.CharField(max_length=100)
    arabic_name = models.CharField(max_length=100, null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product_special_menu(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    special_field = models.ForeignKey(Special_menu, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.special_field.name}"

class discount(models.Model):
    name = models.CharField(max_length=100)
    arabic_name = models.CharField(max_length=100, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product_discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount = models.ForeignKey(discount, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.product.name} - {self.discount.name}"

class Tags(models.Model):
    name = models.CharField(max_length=100)
    arabic_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product_tag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.category.name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "قيد التجهيز"),
        ("shipping", "قيد الشحن"),
        ("delivered", "تم التوصيل"),
        ("cancelled", "ملغي"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CartManger()