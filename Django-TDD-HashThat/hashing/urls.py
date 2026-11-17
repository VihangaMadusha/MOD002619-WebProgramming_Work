from django.urls import path

from . import views

app_name = "hashing"

urlpatterns = [
    path("", views.home, name="home"),
    path("hash/<str:hash>", views.hash, name="hash"),
    path("quickhash", views.quickhash, name="quickhash"),
]
