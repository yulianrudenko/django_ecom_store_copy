from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from ecommerce.apps.catalogue import models

from .basket import Basket


def basket_summary(request):
    basket = Basket(request).__iter__()
    context = {"basket_iterable": basket}
    return render(request, "basket/summary.html", context)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "POST":
        product_id = int(request.POST.get("productId"))
        product_qty = int(request.POST.get("productQty"))
        product = get_object_or_404(models.Product, id=product_id)
        basket.add(product=product, product_qty=product_qty)
    basket_qty = basket.__len__()
    response = JsonResponse({"qty": basket_qty})
    return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "POST":
        product_id = str(request.POST.get("productId"))
        basket.delete(product_id=product_id)
    basket_qty = basket.__len__()
    response = JsonResponse({"qty": basket_qty, "subtotal": basket.get_subtotal_price()})
    return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "POST":
        product_id = str(request.POST.get("productId"))
        product_qty = int(request.POST.get("productQty"))
        basket.update(product_id=product_id, product_qty=product_qty)
    basket_qty = basket.__len__()
    response = JsonResponse({"qty": basket_qty, "subtotal": basket.get_subtotal_price()})
    return response
