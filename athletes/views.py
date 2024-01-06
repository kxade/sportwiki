from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Athlete, Category, TagPost, UploadFiles
from uuid import uuid4

from .utils import DataMixin


class AthleteHome(DataMixin, ListView):
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Athlete.published.all().select_related('cat')


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    #model = Athlete
    #fields = '__all__'
    template_name = "athletes/addpage.html"
    title_page = "Добавление статьи"
    #success_url = reverse_lazy('home')


class UpdatePage(DataMixin, UpdateView):
    model = Athlete
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = "athletes/addpage.html"
    title_page = "Редактирование статьи"
    #success_url = reverse_lazy('home')


def contact(request):
    return HttpResponse(f"Обратная связь")

def login(request):
    return HttpResponse(f"Авторизация")

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request,
                  "athletes/about.html",
                  {'title': 'О сайте', 'form': form})


class ShowPost(DataMixin, DetailView):
    #model = Athlete
    template_name = 'athletes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title, cat_selected=context['post'].cat.pk)

    def get_object(self, queryset=None):
        return get_object_or_404(Athlete.published, slug=self.kwargs[self.slug_url_kwarg])


class AthleteCategory(DataMixin, ListView):
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Athlete.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


class TagPostList(DataMixin, ListView):
    template_name = 'athletes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Athlete.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тэг - ' + tag.tag)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# функция для загрузки файлов без привязки к модели
# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}{uuid4}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)