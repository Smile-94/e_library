from django import forms

from apps.book.models.category_model import Category, SubCategory
from apps.common.widgets import CustomPictureImageFieldWidget


class CategoryForm(forms.ModelForm):
    category_image = forms.ImageField(widget=CustomPictureImageFieldWidget)

    class Meta:
        model = Category
        fields = [
            "category_name",
            "category_image",
            "active_status",
            "description",
        ]
        widgets = {
            "category_name": forms.TextInput(attrs={"placeholder": "Category Name"}),
            "active_status": forms.Select(attrs={"placeholder": "Active Status"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }


class SubCategoryForm(forms.ModelForm):
    sub_category_image = forms.ImageField(widget=CustomPictureImageFieldWidget)

    class Meta:
        model = SubCategory
        fields = ["category", "sub_category_name", "sub_category_image", "active_status", "description"]
        widgets = {
            "sub_category_name": forms.TextInput(attrs={"placeholder": "Sub Category Name"}),
            "active_status": forms.Select(attrs={"placeholder": "Active Status"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }
