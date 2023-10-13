from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Athlete

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


cats_db = [
    {"id": 1, "name": "Борцы"},
    {"id": 2, "name": "Дзюдоисты"},
    {"id": 3, "name": "Бойцы"},
    {"id": 4, "name": "Шахматисты"},
]


def index(request):  #HttpRequest
    posts = Athlete.published.all()

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'athletes/index.html', context=data)

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse(f"Обратная связь")

def login(request):
    return HttpResponse(f"Авторизация")

def about(request):
    return render(request, "athletes/about.html", {'title': 'О сайте', 'menu': menu})

def show_post(request, post_slug):

    post = get_object_or_404(Athlete, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'athletes/post.html', data)

def show_category(request, cat_id):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': db,
        'cat_selected': cat_id,
    }
    return render(request, 'athletes/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

