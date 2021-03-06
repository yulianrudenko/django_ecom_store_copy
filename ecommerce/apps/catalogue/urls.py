from django.urls import path

from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.store_home, name="store_home"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
    path("shop/<slug:slug>/", views.category_list, name="category_list"),
]
