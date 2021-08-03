from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'create_date',  'published', 'get_photo', 'visits',) # эти поля будут отображаться в админке
    list_display_links = ('id', 'title') # на эти поля будут ссылки для переда к объекту
    search_fields = ('title', 'content') # по этим полям будет поиск
    list_editable = ('published', 'category')
    list_filter = ('published', 'category', 'tag')
    save_on_top = True
    save_as = True
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }

    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f"<img src ='{obj.photo.url}' width='70'>")
        else:
            return '-'
    get_photo.short_description = 'фото'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'date',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_category',)
    list_display_links = ('id', 'title_category')
    save_as = True
    save_on_top = True
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }


class TagAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}  # в поле slug дубируется название из tilte транслитом
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", 'post', 'create_comment')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Subscribe,SubscribeAdmin)
admin.site.register(Comment,CommentAdmin)
# Register your models here.
