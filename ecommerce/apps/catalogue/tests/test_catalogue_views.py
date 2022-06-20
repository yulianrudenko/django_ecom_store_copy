import pytest
from django.urls import reverse
from ecommerce.apps.catalogue import views


@pytest.mark.django_db
def test_root_url(client):
    url = reverse("catalogue:store_home")
    response = client.get(url)
    assert response.status_code == 200
