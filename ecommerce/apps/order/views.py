from django.http.response import JsonResponse
from django.shortcuts import render
from ecommerce.apps.basket.basket import Basket

from . import models


def add(request):
    basket = Basket(request)
    if request.POST.get("action") == "POST":
        user_id = request.user.id
        order_key = request.POST.get("order_key")
        baskettotal = basket.get_total_price()
        if models.Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = models.Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk
            for item in basket:
                models.OrderItem.objects.create(
                    order=order, product=item["product"], price=item["price"], quantity=item["qty"]
                )
        response = JsonResponse({"success": "Return something"})
        return response


def payment_confirmation(data):
    try:
        models.Order.objects.filter(order_key=data).update(billing_status=True)
    except:
        raise ValueError("Order doesn't exist")


def get_user_orders(user_id):
    user_id = user_id
    return models.Order.objects.filter(user_id=user_id).filter(billing_status=True)
