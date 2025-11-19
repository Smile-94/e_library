import re
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

# models
from apps.account.models.user_model import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "contact_no",
            "gender",
            "profile_photo",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")

        # Optional: prevent duplicate email
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")

        return email

    def clean_contact_no(self):
        contact = self.cleaned_data.get("contact_no")

        if not contact:
            raise ValidationError("Phone number is required.")

        # BD phone validation: accept 01XXXXXXXXX or +8801XXXXXXXXX
        pattern = r"^(01[3-9]\d{8}|(\+8801[3-9]\d{8}))$"

        if not re.match(pattern, contact):
            raise ValidationError("Enter a valid Bangladeshi phone number.")

        return contact

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match. Please enter the same password in both fields.")

        return cleaned_data
