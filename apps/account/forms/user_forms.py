from django import forms
from django.core.exceptions import ValidationError

from apps.account.models.user_model import User

# Custom widgets
from apps.common.widgets import CustomPictureImageFieldWidget


# <<------------------------------------>>> Create Staff Form <<------------------------------------>>
class StaffForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=CustomPictureImageFieldWidget, required=False)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True, min_length=6, label="Password"
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True, label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "contact_no",
            "gender",
            "profile_photo",
            "is_active",
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True

        if commit:
            user.save()
        return user


# <<--------------------------------- Staff Update Form ------------------------------------>>
class UserForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=CustomPictureImageFieldWidget, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "contact_no",
            "gender",
            "profile_photo",
            "is_active",
        ]


class EditMyProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "contact_no",
            "gender",
            "profile_photo",
        ]
