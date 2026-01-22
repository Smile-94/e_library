from django import forms

from apps.account.models.user_model import User
from apps.book.models.book_model import Book, DownloadTypeChoices
from apps.common.widgets import CustomPictureImageFieldWidget


class BookForm(forms.ModelForm):
    book_image = forms.ImageField(widget=CustomPictureImageFieldWidget)
    publication_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}), required=False)

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "category",
            "book_image",
            "isbn",
            "language",
            "publication_date",
            "edition",
            "digital_file",
            "preview_file",
            "digital_price",
            "physical_price",
            "purchase_price",
            "has_physical_copy",
            "status",
            "is_read_only",
            "is_downloadable",
            "download_type",
            "active_status",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # show only authors
        self.fields["author"].queryset = User.objects.filter(is_author=True)

    def clean(self):
        cleaned_data = super().clean()
        download_type = cleaned_data.get("download_type")
        digital_price = cleaned_data.get("digital_price")
        physical_price = cleaned_data.get("physical_price")
        has_physical_copy = cleaned_data.get("has_physical_copy")
        is_read_only = cleaned_data.get("is_read_only")
        digital_file = cleaned_data.get("digital_file")

        # Only validate prices if download_type is not free
        if download_type != "free":
            if not digital_price or digital_price <= 0:
                self.add_error("digital_price", "Digital price must be greater than zero for paid downloads.")

        if download_type == DownloadTypeChoices.PAID and not cleaned_data.get("is_downloadable"):
            self.add_error("is_downloadable", "Paid books must be downloadable.")

        # If physical copy exists, physical price must be > 0
        if has_physical_copy:
            if not physical_price or physical_price <= 0:
                self.add_error("physical_price", "Physical price must be greater than zero if book has a physical copy.")

        # If read-only, digital file must be provided
        if is_read_only:
            if not digital_file:
                self.add_error("digital_file", "Digital file is required for read-only books.")

        return cleaned_data
