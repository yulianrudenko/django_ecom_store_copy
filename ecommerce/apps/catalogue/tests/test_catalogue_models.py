import pytest
from django.urls import reverse


def test_category_str_method(product_category):
    assert str(product_category) == "django"


def test_category_get_absolute_url(client, product_category):
    url = reverse("catalogue:category_list", args=[product_category.slug])
    response = client.get(url)
    assert response.status_code == 200


def test_product_type_str_method(product_type):
    assert str(product_type) == "book"


def test_product_specification_str_method(product_specification):
    assert str(product_specification) == "pages"


def test_product_str_method(product):
    assert str(product) == "product_title"


def test_product_get_absolute_url(client, product):
    url = product.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200


def test_product_specification_value_str_method(product_specification_value):
    assert str(product_specification_value) == "100"
