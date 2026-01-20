from django import forms

from apps.account.models.user_model import User
from apps.book.models.book_model import Book
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
            "active_status",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # show only authors
        self.fields["author"].queryset = User.objects.filter(is_author=True)
