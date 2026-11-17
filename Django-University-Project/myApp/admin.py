from django.contrib import admin

from .models import Module, Student

admin.site.register(Student)
admin.site.register(Module)
