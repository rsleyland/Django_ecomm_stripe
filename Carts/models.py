from django.db import models
from Account.models import MyUser
from Products.models import Product


class Cart(models.Model):

    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    date_modified = models.DateTimeField(auto_now=True)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    