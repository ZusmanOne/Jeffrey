from django.test import TestCase
from news.models import *
from django.urls import reverse
from news.views import *


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_news = 14
        for i in range(number_of_news):
            News.objects.create(title = 'news %s' % i,
                                content = 'connent assssskdnasndoisafiodnifndfindsingdfngisvifsnvinmpbifnbdingin %s'%i,
                                )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('news'))

        self.assertRedirects(resp, status_code=301, target_status_code=200)


    # def test_views_url_index(self):
    #     """этот тест подобен вышенаписанному только в качестве адреса в ф-ии реверс указывается имя урла(news)"""
    #     resp= self.client.get(reverse('news'))
    #     self.assertTrue(resp.status_code==200)

    # def test_used_template_for_index(self):
    #     """этот тест проверяте какой шаблон должен открываться по заданному маршруту"""
    #     resp = self.client.get(reverse('news'))
    #     print(resp.context['news'])
    #     self.assertTemplateUsed(resp, 'news/index.html')
