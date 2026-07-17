from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 60, unique = True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length = 60)
    description = models.CharField(max_length = 200, blank=True, null=True)
    mrp = models.DecimalField(max_digits = 6, decimal_places = 2, null=True)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)
    productImg = models.URLField(null = True) 


    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, null = True, on_delete = models.CASCADE)
    customer = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'