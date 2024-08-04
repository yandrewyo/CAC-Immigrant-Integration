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
        context["module"] = request.GET.get("module")
        context["module_title"] = " ".join(request.GET.get("module").split("-")).title()
    return render(request, "preview.html", context)


def module(request):
    context = {}
    if "module" in request.GET:
        context["module"] = request.GET.get("module")
        context["module_title"] = " ".join(request.GET.get("module").split("-")).title()
        context["module_file_name"] = context["module"] + ".pdf"
    return render(request, "module.html", context)
