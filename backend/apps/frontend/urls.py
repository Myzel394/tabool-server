from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirect),
    path("app", views.index, name="app"),
    path("robots.txt", views.index),
]
