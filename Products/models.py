from django.db import models
from django.apps import apps

class Product(models.Model):

    prod_name = models.CharField(max_length=120, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    order_count = models.IntegerField(default=0)
    ending_date = models.DateTimeField()
    desc = models.TextField()
    thumbnail = models.ImageField(upload_to='images', blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

        #update current cart prices
        Cart = apps.get_model(app_label='Carts', model_name='Cart') #FIXES CIRUCLAR IMPORT

        carts = Cart.objects.all()
        CartItem = apps.get_model(app_label='Carts', model_name='CartItem') #FIXES CIRUCLAR IMPORT

        for cart in carts:
            cart.subtotal = 0.00
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                cart.subtotal += round(cart.subtotal + (float(item.item.price) * float(item.quantity)),2)
                item.total = round(float(item.item.price) * float(item.quantity), 2)
                item.save()
            cart.save()



class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', blank=False)