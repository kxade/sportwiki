from django.contrib import admin
from .models import Athlete, Category

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ('time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 5

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, athlete: Athlete):
        return f"Описание {len(athlete.content)} символов"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')