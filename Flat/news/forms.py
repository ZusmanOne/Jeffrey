from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from django.views.generic import ListView

class AddNews(forms.Form):
    title = forms.CharField(max_length=150, label='Название',
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5
    }))
    published = forms.BooleanField(label='Опубликовано?', initial=True)
    category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Категория', queryset=Category.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))


class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title_category']
        widgets = {
            'title_category': forms.TextInput(attrs={'class':'form-control'})
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
#                    }