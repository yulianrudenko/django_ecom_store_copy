from decimal import Decimal

from django.conf import settings
from django.db import models
from ecommerce.apps.catalogue.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order")
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    post_code = models.CharField(max_length=50)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=150)
    payment_option = models.CharField(max_length=200, blank=True)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.pk}.{self.user}, {self.created}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.pk}.{self.product} x{self.quantity}"
