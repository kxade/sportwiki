from django import forms
from .models import Category, MedCard


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок")
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    medcard = forms.ModelChoiceField(queryset=MedCard.objects.all(), required=False, empty_label="Мед. карта не выбрана", label="Мед. карта")


