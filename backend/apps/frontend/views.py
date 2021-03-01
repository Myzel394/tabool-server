from django.shortcuts import redirect as url_redirect, render


def redirect(request):
    return url_redirect("app")


def index(request):
    return render(request, "frontend/index.html")


def robots(request):
    return "User-agent: *\nDisallow: /"
