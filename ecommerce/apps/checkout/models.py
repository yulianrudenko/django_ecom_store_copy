from django.db import models
from django.utils.translation import gettext_lazy as _
from ecommerce.apps.order.models import Order


class DeliveryOptions(models.Model):
    DELIVERY_CHOICES = [
        ("IS", "In Store"),
        ("HD", "Home Delivery"),
        ("DD", "Digital Delivery"),
    ]
    name = models.CharField(
        verbose_name=_("delivery name"),
        help_text=_("Required"),
        max_length=255,
    )
    price = models.DecimalField(
        verbose_name=_("delivery price"),
        help_text=_("Required"),
        max_digits=5,
        error_messages={"name": {"max_length": _("Price must be between 0 and 999")}},
        decimal_places=2,
    )
    method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("delivery method"),
        help_text=_("Required"),
        max_length=255,
    )
    timeframe = models.CharField(
        verbose_name=_("delivery timeframe"),
        help_text=_("Required"),
        max_length=255,
    )
    window = models.CharField(
        verbose_name=_("delivery window"),
        help_text=_("Required"),
        max_length=255,
    )
    order_self = models.IntegerField(
        verbose_name=_("list order"),
        help_text=_("Required"),
        default=0,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self) -> str:
        return f"{self.name}"


# class PaymentSelections(models.Model):
#     name = models.CharField(
#         verbose_name=_("payment name"),
#         help_text=_("Required"),
#         max_length=255,
#     )
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name = _("Payment Selection")
#         verbose_name_plural = _("Payment Selections")

#     def __str__(self) -> str:
#         return f"{self.name}"
