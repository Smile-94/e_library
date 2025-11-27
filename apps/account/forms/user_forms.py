from django import forms
from apps.account.models.user_model import User

# Custom widgets
from apps.common.widgets import CustomPictureImageFieldWidget


class UserForm(forms.ModelForm):
    profile_photo = forms.ImageField(widget=CustomPictureImageFieldWidget)

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
