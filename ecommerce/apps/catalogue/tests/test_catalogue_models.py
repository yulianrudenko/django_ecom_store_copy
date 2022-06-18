import pytest


def test_category_str_method(product_category):
    assert str(product_category) == "django"
