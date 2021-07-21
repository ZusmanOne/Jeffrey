"""
здесь будут создаваться кастомные теги, они нужны для того что бы не создавать один и тот же функционал который треуется
в разныъ контроллерах(вьюхах).Например на разных шаблонах нужен один  тот же кверисет, для этого можно
 создать его в  тегах и применять в разных шаблонах, после того как написан тег его нужно подгрузить в шаблон через "load"
 и затем включить через метод as, пример: {% category_object as qwerty %}
"""
from news.models import Category
from django import template
register = template.Library()
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@register.simple_tag(name='my_tag') #здесь используется простой тег
def category_object():
    return Category.objects.all()


@register.inclusion_tag('news/list_category_tag.html') # здесь создается тег сразу с собственным шаблоном
def list_category():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories, 20)
    return {'categories': categories}