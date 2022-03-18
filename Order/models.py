from django.db import models
from django.conf import settings
from Products.models import Product


class Order(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    date_added = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_added']


class OrderItem(models.Model):

    from_order = models.ForeignKey(Order,related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.Case)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        order = self.from_order
        order.subtotal += round(float(self.product.price) * float(self.quantity),2)
        order.save()
        temp = round(float(self.product.price) * float(self.quantity),2)
        self.subtotal = temp
        self.total = round((temp * 1.15),2)
        super().save(*args, **kwargs)