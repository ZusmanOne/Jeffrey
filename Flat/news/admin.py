from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'create_date', 'update_date', 'published') # эти поля будут отображаться в админке
    list_display_links = ('id', 'title') # на эти поля будут ссылки для переда к объекту
    search_fields = ('title', 'content') # по этим полям будет поиск
    list_editable = ('published', 'category')
    list_filter = ('published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_category',)
    list_display_links = ('id', 'title_category')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)


# Register your models here.
