from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

menu = ["О сайте", "Добавить статью",  "Обратная связь", "Войти"]


def index(request):  #HttpRequest
    data = {'title': 'Главная страница',
            'menu': menu}
    return render(request, 'athletes/index.html', context=data)

def about(request):
    return render(request, "athletes/about.html", {'title': 'О сайте'})

def categories(request, cat_id):  #HttpRequest
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

def categories_by_slug(request, cat_slug):  #HttpRequest
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_slug}</p>")

def archive(request, year):  #HttpRequest
    if year > 2023:
        uri = reverse('cats', args=("wrestlers",))
        return HttpResponseRedirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p>id: {year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

