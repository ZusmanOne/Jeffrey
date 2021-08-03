from django.test import TestCase
from news.forms import *


class TestFormNews(TestCase):
    """тест для проверки праильности названия полей"""
    def test_form_label(self):
        form = AddNews()
        self.assertTrue(form['title'].label == 'Name' or form['title'].label == 'Название')
        self.assertTrue(form['content'].label == 'Текст')


# class TestFormCategory(TestCase):
#     def test_valid_title(self):
#         title = {'title_category':'франшиза'}
#         form_data = AddCategory(title_category=title)
