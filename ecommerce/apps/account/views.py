from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ecommerce.apps.catalogue.models import Product
from ecommerce.apps.order.views import get_user_orders

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, Customer
from .token import account_activation_token


@login_required
def dashboard(request):
    user_orders = get_user_orders(request.user.id)
    return render(request, "account/user/dashboard.html", {"orders": user_orders})


@login_required
def account_edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, "account/user/edit_account.html", {"user_form": user_form})


@login_required
def account_delete(request):
    user = Customer.objects.get(pk=request.user.pk)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_profile_confirmation")


def account_register(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data["email"]
            user.set_password(register_form.cleaned_data["password"])
            user.is_active = False
            user.save()
            # setup activation by email message
            domain = get_current_site(request).domain
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return HttpResponse("Account created, check your email to activate.")
    else:
        register_form = RegistrationForm()
    return render(request, "account/registration/register.html", {"register_form": register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    return render(request, "account/registration/activation_invalid.html")


# Addresses
@login_required
def addresses(request):
    addresses = Address.objects.filter(customer_id=request.user.id)
    context = {"addresses": addresses}
    return render(request, "account/user/address/addresses.html", context)


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(request.POST)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            if not Address.objects.filter(customer_id=request.user.id, is_default=True).exists():
                new_address.is_default = True
            new_address.customer_id = request.user.id
            new_address.save()
            return redirect("account:addresses")
    address_form = UserAddressForm()
    context = {"form": address_form}
    return render(request, "account/user/address/edit_address.html", context)


@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id, customer_id=request.user.id)
    if request.method == "POST":
        address_form = UserAddressForm(request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            return redirect("account:addresses")
    address_form = UserAddressForm(instance=address)
    context = {"form": address_form}
    return render(request, "account/user/address/edit_address.html", context)


@login_required
def delete_address(request, id):
    address = get_object_or_404(Address, id=id, customer_id=request.user.id)
    address.delete()
    return redirect("account:addresses")


@login_required
def set_default_address(request, id):
    Address.objects.filter(customer_id=request.user.id, is_default=True).update(is_default=False)
    Address.objects.filter(id=id, customer_id=request.user.id).update(is_default=True)
    previous_url = request.META.get("HTTP_REFERER")
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")
    return redirect("account:addresses")


@login_required
def wishlist(request):
    wishlist_products = Product.objects.filter(users_wishlist__id=request.user.id)
    context = {"wishlist": wishlist_products}
    print(request.META["HTTP_REFERER"])
    return render(request, "account/user/wishlist.html", context)


@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.warning(request, f"Removed {product.title} from your Wishlist")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, f"Added {product.title} to your Wishlist")
    return redirect(request.META["HTTP_REFERER"])


@login_required
def user_orders(request):
    orders = get_user_orders(request.user.id)
    context = {"orders": orders}
    return render(request, "account/user/orders.html", context)
