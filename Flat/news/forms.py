from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AddNews(forms.Form):
    title = forms.CharField(max_length=150, label='Название',
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5
    }))
    published = forms.BooleanField(label='Опубликовано?', initial=True)
    category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Категория',
                                      queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))
    photo = forms.ImageField(label='Загрузите фото', required=False,)


class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title_category']
        widgets = {
            'title_category': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_title_category(self):
        my_title = self.cleaned_data['title_category']
        all_title = Category.objects.all()
        for i in all_title:
            if i.title_category == my_title:
                raise ValidationError('Такая категория уже существует')
        return my_title


# class DeleteCategory(forms.ModelForm): удаление катгории из выпадающего списка
#     class Meta:
#         models = Category
#         fields = ['title']
#         widgets = {
#             'class':forms.Select(attrs={'class':'form-control'})
#
#

# кастомная форма для регистарции пользователя
# class UserRegistrForm(UserCreationForm):
#     username = forms.CharField(label='Введитя имя пользователя',
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#    password2 = forms.CharField(label='Подвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# ФОРМА ДЛЯ О ПРАВКИ EMAIL ПИСЬМА
class SendForm(forms.Form):
    subject = forms.CharField(label='Тема письма', max_length=200)
    message = forms.CharField(label='Текст сообщения', widget=forms.Textarea(attrs={'class': 'form-control'}))


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email Address'})
        }

    def clean_email(self):
        cleaned_mail = self.cleaned_data['email']
        all_mail = Subscribe.objects.all()
        for i in all_mail:
            if i.email == cleaned_mail:
                print('ПОЧТА УЖЕ ЕСТЬ!!!!!!!!!!!!')
                raise ValueError('Такая почта уже подписана на рассылку')
        return cleaned_mail


class CommentForm(forms.ModelForm): # связнная форма для написания комментов
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {'body':forms.TextInput(attrs={'class':'form-control'})}