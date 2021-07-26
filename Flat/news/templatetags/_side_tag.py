from django import template
from news.models import *


register = template.Library()


@register.inclusion_tag('news/sidebar_right.html')
def list_side():
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    popular_post = News.objects.order_by['-visits']
    context = {'category_list':category_list, 'tag_list': tag_list, 'popular_post':popular_post}
    return context
