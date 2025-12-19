from datetime import date

from django import forms

from apps.author.models.author_model import AuthorEducation


class AuthorEducationForm(forms.ModelForm):
    YEAR_CHOICES = [(y, y) for y in range(1950, date.today().year + 1)]

    start_year = forms.ChoiceField(choices=YEAR_CHOICES)
    end_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)

    class Meta:
        model = AuthorEducation
        fields = ["degree", "institution", "start_year", "end_year"]
