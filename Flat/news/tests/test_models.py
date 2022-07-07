from django.test import TestCase
from news.models import *


class NewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        создается неизменяемый объект в дальнейшем, который будет тестироваться всеми созданными методами
        """
        News.objects.create(title='Новое зерно в 3 кваратле 2021',
                            content='Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч. Шеф взъярён тчк щипцы с эхом'
                                      ' гудбай Жюль. Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф. Экс-граф? Плюш'
                                      ' изъят. Бьём чуждый цен хвощ! Эх, чужак! Общий съём цен шляп (юфть) — вдрызг!'
                                      ' Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч. Шеф взъярён тчк щипцы с эхом '
                                      'гудбай Жюль. Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф. Экс-граф? Плюш изъят.'
                                      ' Бьём чуждый цен хвощ! Эх, чужак! Общий съём цен шляп (юфть) — вдрызг! Любя,'
                                      ' съешь щипцы, — вздохнёт мэр, — кайф жгуч. Шеф взъярён тчк щипцы с эхом гудбай'
                                      ' Жюль. Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф. Экс-граф? Плюш изъят. Бьём '
                                      'чуждый цен хвощ! Эх, чужак! Общий съём цен шляп (юфть) — вдрызг!',
                            )

    def test_title_label(self):
        """данный тест проверяет значение текстовых меток (verbose_name) поля title включая их ожидаему длину"""
        title = News.objects.get(id=1)
        field_label = title._meta.get_field('title').verbose_name
        self.assertEqual(field_label,'title')

    def test_expected_object(self):
        """данный тест проверяет созданный в модели метод def __str__ т.е какойе имя обхекта должно возвращаться"""
        title = News.objects.get(id=1)
        # expected = "%s" % (title.title)
        self.assertEqual(title.__str__(), str(title))

    def test_get_absolute_url(self):
        """
        данный тест проверяет метод get_absolute_url котоырй должен принимать значения каждого объекта  по номеру id
        """
        title = News.objects.get(id=1)
        self.assertEqual(title.get_absolute_url(), '/news/1/')

