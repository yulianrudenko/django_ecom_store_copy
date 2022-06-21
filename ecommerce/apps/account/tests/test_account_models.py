import pytest


def test_customer_str_method(customer):
    assert str(customer) == "user1"


def test_superuser_str_method(admin):
    assert str(admin) == "admin"


def test_customer_no_email_input(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(email="")
    assert str(err.value) == "You must provide an email"


def test_customer_invalid_email_input(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(email="invalid.email@")
    assert str(err.value) == "You must provide a valid email"


def test_admin_staff_False(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(name="admin", is_staff=False, is_superuser=True)
    assert str(err.value) == '"is_staff" must be True for Superuser.'


def test_admin_superuser_False(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(name="admin", is_staff=True, is_superuser=False)
    assert str(err.value) == '"is_superuser" must be True for Superuser.'


def test_address_str_method(address):
    full_name = address.full_name
    assert str(address) == full_name
