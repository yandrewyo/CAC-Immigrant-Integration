from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "index.html")


def timeline(request):
    return render(request, "timeline.html")


def about(request):
    return render(request, "about.html")


def profile(request):
    return render(request, "profile.html")


def preview(request):
    context = {}
    if "module" in request.GET:
        context["module"] = " ".join(request.GET.get("module").split("-")).title()
        print(context["module"])
    return render(request, "preview.html", context)


def module(request):
    context = {}
    return render(request, "module.html", context)
