from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)

from .models import Address, Customer


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(label="Enter name", min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(
        label="Enter email",
        max_length=100,
        help_text="Required",
        error_messages={"required": "You will need an email."},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["placeholder"] = "Name"
        self.fields["email"].widget.attrs.update({"placeholder": "E-mail", "id": "id_email"})
        self.fields["password"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Repeat password"

    class Meta:
        model = Customer
        fields = (
            "name",
            "email",
        )

    def clean_password2(self):
        if self.cleaned_data["password"] != self.cleaned_data["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.all().filter(email=email).exists():
            raise forms.ValidationError("User with given email already exists.")
        return email

    # def clean_username(self):
    #     user_name = self.cleaned_data["user_name"].lower()
    #     if Customer.objects.all().filter(user_name=user_name).exists():
    #         raise forms.ValidationError("User with given username already exists.")
    #     return user_name


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placceholder": "Email",
                "id": "login-email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placceholder": "Password",
                "id": "login-password",
            }
        )
    )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email", "readonly": "readonly"}
        ),
    )
    name = forms.CharField(
        label="Name",
        min_length=4,
        max_length=60,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Name", "id": "form-name"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["email"].widget.attrs["readonly"] = True
        self.fields["name"].required = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Customer.objects.all().filter(email=email).exists():
            raise forms.ValidationError("User with given email already exists.")
        return email

    class Meta:
        model = Customer
        fields = ("email", "name")


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=160,
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "email", "id": "form-email"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = Customer.objects.all().filter(email=email)
        if not user:
            raise forms.ValidationError("User with given email does not exist.")
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "Password", "id": "new-password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm new Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-3", "placeholder": "New Password", "id": "new-password2"}
        ),
    )


class UserAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full name"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Phone number"}
        )
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Second address"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Town/City"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Post code"}
        )

    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]
