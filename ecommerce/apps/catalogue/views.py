from django.shortcuts import get_object_or_404, render

from . import models


def store_home(request):
    products = models.Product.objects.prefetch_related("product_image").filter(is_active=True)
    context = {"products": products}
    return render(request, "catalogue/index.html", context)


def product_detail(request, slug):
    context = {"product": get_object_or_404(models.Product, slug=slug, is_active=True)}
    return render(request, "catalogue/product.html", context)


def category_list(request, slug):
    category = get_object_or_404(models.Category, slug=slug)
    products = models.Product.objects.filter(category__in=category.get_descendants(include_self=True))
    print(models.Category.objects.get(name="Shoes").get_descendants())
    return render(request, "catalogue/category.html", {"category": category, "products": products})
