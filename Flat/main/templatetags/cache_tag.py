# from django.contrib.flatpages.models import *
# from django.core.cache import cache
# from django import template
#
# register = template.Library()
#
# #
# # @register.simple_tag(name='cache_tag')
# # def cache_tag():
# #     flat = cache.get('flat')
# #     if not flat:
# #         flat = FlatPage.objects.filter()
# #         cache.set('flat',flat, 20)
# #     return {'flat': flat}
