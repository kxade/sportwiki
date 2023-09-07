from django.http import HttpResponse
from django.shortcuts import render


def index(request):  #HttpRequest
    return HttpResponse("Страница приложения Athletes.")


def categories(request):  #HttpRequest
    return HttpResponse("Статьи по категориям")