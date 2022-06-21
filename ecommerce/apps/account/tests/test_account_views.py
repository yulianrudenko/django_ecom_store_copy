import pytest
from django.urls import reverse


def test_dashboard_response(client, customer):
    user = customer
    client.force_login(user)
    response = client.get("/account/dashboard/")
    assert response.status_code == 200


# def test_account_edit_response(client, customer):
#     user = customer
#     client.force_login(user)
#     response = client.get("/account/dashboard/")
#     assert response.status_code == 200
