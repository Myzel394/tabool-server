from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.redirect),
    re_path(r"app/(?:.*)/?$", views.index, name="app"),
    path("robots.txt", views.index),
]
