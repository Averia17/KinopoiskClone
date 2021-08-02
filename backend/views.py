from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


def main_page(request):
    template_name = 'index.html'
    return render(request, template_name, {})


def film_detail(request, id):
    template_name = 'index.html'
    return render(request, template_name, {})


def serial_detail(request, id):
    template_name = 'index.html'
    return render(request, template_name, {})


def staff_detail(request, id):
    template_name = 'index.html'
    return render(request, template_name, {})


def serials(request):
    template_name = 'index.html'
    return render(request, template_name, {})


def films(request):
    template_name = 'index.html'
    return render(request, template_name, {})


def country_detail(request, slug):
    template_name = 'index.html'
    return render(request, template_name, {})


def genre_detail(request, slug):
    template_name = 'index.html'
    return render(request, template_name, {})