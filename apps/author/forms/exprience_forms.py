from django import forms

from apps.author.models.author_model import AuthorWorkExperience


class AuthorWorkExperienceForm(forms.ModelForm):
    class Meta:
        model = AuthorWorkExperience
        fields = [
            "job_title",
            "organization",
            "start_date",
            "end_date",
            "description",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter your work experience here..."}),
        }
