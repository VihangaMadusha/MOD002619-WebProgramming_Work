from django import forms

from .models import Student


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["firstName", "lastName", "age", "email", "enrolmentDate", "modules", "image"]
        widgets = {
            # date-time picker widget
            "enrolmentDate": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }
