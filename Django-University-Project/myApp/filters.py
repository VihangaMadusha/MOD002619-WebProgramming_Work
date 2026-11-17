import django_filters

from .models import Student


class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = {
            "firstName": ["icontains"],
            "lastName": ["icontains"],
            "age": ["lt", "gt"],
            "modules__code": ["exact"],
            "modules__name": ["icontains"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # nicer labels than the defaults
        self.form.fields["firstName__icontains"].label = "First Name"
        self.form.fields["lastName__icontains"].label = "Last Name"
        self.form.fields["age__lt"].label = "Age less than"
        self.form.fields["age__gt"].label = "Age greater than"
        self.form.fields["modules__code"].label = "Module Code"
        self.form.fields["modules__name__icontains"].label = "Module Name"
