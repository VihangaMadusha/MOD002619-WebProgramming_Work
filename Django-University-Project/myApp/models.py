from django.db import models


class Module(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code.upper()} {self.name.title()}"


class Student(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(blank=True)
    enrolmentDate = models.DateTimeField()
    modules = models.ManyToManyField("Module", blank=True)
    # Week 05 - only the path is stored in the database; blank=True keeps old rows valid
    image = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return self.firstName.capitalize() + ", " + self.lastName.upper()
