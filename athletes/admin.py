from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Athlete, Category


class MedCardFilter(admin.SimpleListFilter):
    title = 'Наличие медкарты'
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ('medcard', "Есть медкарта"),
            ('nomedcard', "Нет медкарты"),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'medcard':
            return queryset.filter(medcard__isnull=False)
        if self.value() == 'nomedcard':
            return queryset.filter(medcard__isnull=True)

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags')
   #exclude = вариант для исключения полей
    readonly_fields = ['post_photo']#поля только для чтения
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
   #filter_vertical = вертикальный вид выбора
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ('time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ('set_published', 'set_draft')
    search_fields = ('title', 'cat__name')
    list_filter = (MedCardFilter, 'cat__name', 'is_published')
    save_on_top = True

    @admin.display(description="Изображение", ordering="content")
    def post_photo(self, athlete: Athlete):
        if athlete.photo:
            return mark_safe(f'<img src="{athlete.photo.url}" "width=50">')
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Athlete.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Athlete.Status.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')