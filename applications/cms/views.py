from .models import Pages
from django.shortcuts import render


def pages_list(request, condominium_slug):
    pages = Pages.objects.filter(condominium__slug=condominium_slug).all()
    return render(request, 'pages_list.html', {'pages': pages})


def show_page(request, condominium_slug, path):
    page = Pages.objects.filter(condominium__slug=condominium_slug).filter(slug=path).first()
    return render(request, 'page.html', {'page': page})
