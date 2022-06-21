import pytest
from django.forms import ValidationError
from ecommerce.apps.account.forms import (
    MyPasswordResetForm,
    RegistrationForm,
    UserAddressForm,
    UserEditForm,
)


@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, valid",
    [
        ("mike", "02343343434", "add1", "add2", "town", "postcode", True),
        ("", "02343343434", "add1", "add2", "town", "postcode", False),
    ],
)
def test_address_add_form(full_name, phone, address_line, address_line2, town_city, postcode, valid):
    address_form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode,
        }
    )
    assert address_form.is_valid() is valid


@pytest.mark.parametrize(
    "name, email, password, password2, valid",
    [
        ("mikeowen", "mikeowen@gmail.com", "zaq1@WSX", "zaq1@WSX", True),
        ("mikeowen", "wrong_email.com", "zaq1@WSX", "zaq1@WSX", False),
        ("mikeowen", "mikeowen@gmail.com", "zaq1@WSX", "new_password", False),
        ("mik", "mikeowen@gmail.com", "zaq1@WSX", "zaq1@WSX", False),
    ],
)
@pytest.mark.django_db
def test_registration_form(name, email, password, password2, valid):
    registration_form = RegistrationForm(
        data={
            "name": name,
            "email": email,
            "password": password,
            "password2": password2,
        }
    )
    assert registration_form.is_valid() is valid


@pytest.mark.django_db
def test_registration_form_clean_email(customer_factory):
    user = customer_factory.create()
    registration_form = RegistrationForm(
        {
            "name": "user121",
            "email": "user1@gmail.com",
            "password": "zaq1@WSX",
            "password2": "zaq1@WSX",
        }
    )
    assert "User with given email already exists." in registration_form.errors.as_text()


@pytest.mark.django_db
def test_registration_form_clean_password2():
    registration_form = RegistrationForm(
        {
            "name": "user121",
            "email": "user1@gmail.com",
            "password": "zaq1@WSX",
            "password2": "different_password",
        }
    )
    assert "Passwords do not match." in registration_form.errors.as_text()


@pytest.mark.parametrize(
    "name, email, valid",
    [
        ("mike", "newemail@gmail.com", True),
        ("mikeowen", "wrong_email.com", False),
        ("mik", "newemail@gmail.com", False),
    ],
)
@pytest.mark.django_db
def test_user_edit_form(name, email, valid, customer_factory):
    user = customer_factory.create()
    user_edit_form = UserEditForm(
        instance=user,
        data={
            "name": name,
            "email": email,
        },
    )
    assert user_edit_form.is_valid() is valid


@pytest.mark.django_db
def test_user_edit_form_clean_email(customer_factory):
    user = customer_factory.create()
    user_edit_form = UserEditForm(
        {
            "name": "user121",
            "email": "user1@gmail.com",
        }
    )
    assert "User with given email already exists." in user_edit_form.errors.as_text()


@pytest.mark.django_db
def test_password_reset_form_clean_email(customer_factory):
    password_reset_form = MyPasswordResetForm(
        {
            "email": "random_address@gmail.com",
        }
    )
    assert "User with given email does not exist." in password_reset_form.errors.as_text()
    user = customer_factory.create()
    password_reset_form = MyPasswordResetForm(
        {
            "email": "user1@gmail.com",
        }
    )
    assert password_reset_form.is_valid() is True
