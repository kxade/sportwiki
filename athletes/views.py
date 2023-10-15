from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Athlete, Category, TagPost

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
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

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Athlete.published.filter(cat_id=category.pk)
    data = {
        'title': f"Категория: {category.name}",
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'athletes/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Athlete.Status.PUBLISHED)

    data = {
        'title': f"Тэг: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'athletes/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


