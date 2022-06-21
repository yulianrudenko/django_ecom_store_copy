import pytest
from django.urls import reverse


def user_login(client, customer):
    client.force_login(customer)
    return customer


def test_dashboard_response(client, customer):
    user = user_login(client, customer)
    url = reverse("account:dashboard")
    response = client.get(url)
    assert response.status_code == 200


def test_account_edit_response(client, customer):
    url = reverse("account:account_edit")
    user = user_login(client, customer)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_account_edit_post(client, customer_factory):
    customer = customer_factory.create()
    user_login(client, customer)
    url = reverse("account:account_edit")
    response = client.post(url, data={"name": "asss"})
    assert response.status_code == 200


def test_account_delete(client, customer):
    user_login(client, customer)
    url = reverse("account:account_delete")
    response = client.get(url)
    assert response.status_code == 302


def test_addresses_response(client, customer):
    user_login(client, customer)
    url = reverse("account:addresses")
    response = client.get(url)
    assert response.status_code == 200


def test_wishlist_response(client, customer):
    user_login(client, customer)
    url = reverse("account:wishlist")
    response = client.get(url)
    assert response.status_code == 200


def test_user_orders_response(client, customer):
    user_login(client, customer)
    url = reverse("account:user_orders")
    response = client.get(url)
    assert response.status_code == 200
