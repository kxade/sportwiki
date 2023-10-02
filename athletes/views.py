from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

db = [
    {"id": 1, "title": "Хабиб Нурмагомедов", 'content': "Биография Хабиба Нурмагомедова", "is_published": True},
    {"id": 2, "title": "Абдулрашид Саадулаев", 'content': "Биография Абдулрашида Саадулаева", "is_published": False},
    {"id": 3, "title": "Ахмед Тажутдинов", 'content': "Биография Ахмеда Тажутдинова", "is_published": True},
]


def index(request):  #HttpRequest
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': db,
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

def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

