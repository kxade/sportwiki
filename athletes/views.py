from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render


def index(request):  #HttpRequest
    return HttpResponse("Страница приложения Athletes.")


def categories(request, cat_id):  #HttpRequest
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):  #HttpRequest
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_slug}</p>")

def archive(request, year):  #HttpRequest
    if year > 2023:
        raise Http404()
    return HttpResponse(f"<h1>Архив по годам</h1><p>id: {year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")