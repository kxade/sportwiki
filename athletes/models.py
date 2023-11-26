from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Athlete.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=150, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Athlete(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, 'Опубликовано'


    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name="posts", verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="")
    medcard = models.OneToOneField('MedCard', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="athlete", verbose_name="Медкарта")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Известные атлеты"
        verbose_name_plural = "Известные атлеты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class MedCard(models.Model):
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    birthday = models.DateField(null=True)

    def __str__(self):
        return f"Рост: {self.height}; вес: {self.weight}; дата рождения: {self.birthday};"