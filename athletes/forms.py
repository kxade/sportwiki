from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, MedCard, Athlete


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧЦШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхчцшщьыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

# class AddPostForm(forms.Form):                  форма не связанная с моделью
#     title = forms.CharField(max_length=255, min_length=5,
#                             label="Заголовок",
#                             validators = [
#                                 RussianValidator(),
#                             ],
#                             error_messages={
#                                 'min_length': "Слишком короткий заголовок",
#                                 'required': "Без заголовка никак",
#                             })
#     slug = forms.SlugField(max_length=255, label="URL",
#                            validators=[
#                                MinLengthValidator(5, message="Минимум 5 символов"),
#                                MaxLengthValidator(100, message="Максимум 100 символов")
#                            ])
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}), required=False, label="Контент")
#     is_published = forms.BooleanField(required=False, initial=True, label="Статус")
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
#     medcard = forms.ModelChoiceField(queryset=MedCard.objects.all(), required=False, empty_label="Мед. карта не выбрана", label="Мед. карта")


    #при валидации единичного поля
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЧЦШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхчцшщьыъэюя0123456789- "
    #
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")


class AddPostForm(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    medcard = forms.ModelChoiceField(queryset=MedCard.objects.all(), required=False, empty_label="Мед. карта не выбрана", label="Мед. карта")

    class Meta:
        model = Athlete
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': "URL"}


    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов.")

        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")

