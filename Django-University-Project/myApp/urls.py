from django.urls import path

from . import views

app_name = "myApp"

urlpatterns = [
    path("", views.home, name="home"),
    path("studentlist/<int:page>/", views.studentlist, name="studentlist"),
    path("modules/", views.modulelist, name="modulelist"),
    path("student/<int:student_id>/", views.student_detail, name="student_detail"),
    path("student/<int:student_id>/edit/", views.student_edit, name="student_edit"),
]
