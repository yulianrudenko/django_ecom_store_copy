import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from ecommerce.apps.account.models import Address
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.order.models import Order, OrderItem

from .models import DeliveryOptions


@login_required
def delivery_choices(request):
    if len(request.session.get(settings.BASKET_SESSION_ID, -1)) > 0:
        delivery_options = DeliveryOptions.objects.filter(is_active=True)
        context = {"delivery_options": delivery_options}
        if "purchase" in request.session:
            session = request.session
            previous_delivery_option_id = session["purchase"]["delivery_option_id"]
            context["previous_delivery_option_id"] = previous_delivery_option_id
        return render(request, "checkout/delivery_options.html", context)
    messages.warning(request, "Please select products to buy first.")
    return redirect("basket:basket_summary")


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option_id = int(request.POST.get("delivery_option_id"))
        delivery_option = DeliveryOptions.objects.get(id=delivery_option_id)
        updated_total_price = basket.update_delivery(delivery_option.price)
        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_option_id": delivery_option_id,
            }
        else:
            session["purchase"]["delivery_option_id"] = delivery_option_id
            session.modified = True
        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_option.price})
        return response


@login_required
def delivery_address(request):
    if len(request.session.get(settings.BASKET_SESSION_ID, -1)) < 0:
        messages.warning(request, "Please select products to buy first.")
        return redirect("basket:basket_summary")
    if "purchase" not in request.session:
        messages.warning(request, "Please select delivery option first.")
        return redirect("checkout:delivery_choices")
    addresses = Address.objects.filter(customer_id=request.user.id).order_by("-is_default")
    session = request.session
    if addresses:
        if "address" not in session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True
    context = {"addresses": addresses}
    return render(request, "checkout/delivery_address.html", context)


@login_required
def payment_selection(request):
    if len(request.session.get(settings.BASKET_SESSION_ID, -1)) < 0:
        messages.warning(request, "Please select products to buy first.")
        return redirect("basket:basket_summary")
    if "purchase" not in request.session:
        messages.warning(request, "Please select delivery option first.")
        return redirect("checkout:delivery_choices")
    if "address" not in request.session:
        messages.warning(request, "Please select delivery address first.")
        return redirect("checkout:delivery_address")

    context = {}
    return render(request, "checkout/payment_selection.html", context)


###############
#   PAYPAL    #
###############
from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient


@login_required
def payment_complete(request):
    PPClient = PayPalClient()
    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id
    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)
    total_paid = response.result.purchase_units[0].amount.value
    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        post_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.id
    for item in basket:
        OrderItem.objects.create(order_id=order.id, product=item["product"], price=item["price"], quantity=item["qty"])
    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html")
