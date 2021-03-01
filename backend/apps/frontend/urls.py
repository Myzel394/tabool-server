from django.urls import path

from . import views

urlpatterns = [
    path("app/", views.index),
    path("robots.txt", views.index),
]
