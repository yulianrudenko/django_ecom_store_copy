from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import MyPasswordResetForm, PasswordResetConfirmForm, UserLoginForm

app_name = "account"

urlpatterns = [
    # Account interactions
    path("dashboard/", views.dashboard, name="dashboard"),  # redirected there after registration
    path("edit/", views.account_edit, name="account_edit"),
    path("delete_profile/", views.account_delete, name="account_delete"),
    path(
        "delete_profile_confirmation/",
        TemplateView.as_view(template_name="account/user/delete_profile_confirmation.html"),
        name="delete_profile_confirmation",
    ),
    # Password reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password_reset/password_reset_email.html",
            form_class=MyPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_email_confirm",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset/password_reset_confirm.html",
            success_url="/account/password_reset_complete/",
            form_class=PasswordResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_complete",
    ),
    # Authorization
    path("register/", views.account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/registration/login.html", form_class=UserLoginForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/account/login/"), name="logout"),
    # Addresses
    path("addresses/", views.addresses, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default_address, name="set_default_address"),
    # Wish list
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add/<int:product_id>/", views.wishlist_add, name="wishlist_add"),
    path("orders/", views.user_orders, name="user_orders"),
]
