from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import AddPostForm, UploadFileForm
from .models import Athlete, Category, TagPost, UploadFiles
from uuid import uuid4

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]

# def index(request):  #HttpRequest
#     posts = Athlete.published.all().select_related('cat')
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'athletes/index.html', context=data)


class AthleteHome(ListView):
    #model = Athlete
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    extra_context = data = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Athlete.published.all().select_related('cat')


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Главная страница"
    #     context['menu'] = menu
    #     context['posts'] = Athlete.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Athlete.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Ошибка добавления поста")
#             form.save() # доступно при использовании формы связанной с моделью
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#
#     }
#     return render(request, 'athletes/addpage.html', context=data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {'menu': menu,
                'title': 'Добавление статьи',
                'form': form
                }
        return render(request, 'athletes/addpage.html', context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {'menu': menu,
                'title': 'Добавление статьи',
                'form': form
        }
        return render(request, 'athletes/addpage.html', context=data)


def contact(request):
    return HttpResponse(f"Обратная связь")

def login(request):
    return HttpResponse(f"Авторизация")


# функция для загрузки файлов без привязки к модели
# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}{uuid4}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)



def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()


    return render(request, "athletes/about.html", {'title': 'О сайте', 'menu': menu,
                                                   'form': form})

# def show_post(request, post_slug):
#
#     post = get_object_or_404(Athlete, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'athletes/post.html', data)


class ShowPost(DetailView):
    #model = Athlete
    template_name = 'athletes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        context['cat_selected'] = context['post'].cat.pk
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Athlete.published, slug=self.kwargs[self.slug_url_kwarg])
def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Athlete.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f"Категория: {category.name}",
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'athletes/index.html', context=data)


class AthleteCategory(ListView):
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Athlete.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

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

class TagPostList(ListView):
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Athlete.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тэг - ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


