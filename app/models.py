from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Province 1', 'Province 1'),
    ('Province 2', 'Province 2'),
    ('Province 3', 'Province 3'),
    ('Province 4', 'Province 4'),
    ('Province 5', 'Province 5'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('JE', 'Jeans'),
    ('S','Shoes'),
    ('SH','Shirts'),
    ('J','Jackets'),
    ('Tr','Trousers'),
    ('OP', 'One Piece'),
    ('LS', 'Ladies Shoes'),
    ('LP', 'Ladies Pants'),
    ('TO', 'Tops'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Preorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price