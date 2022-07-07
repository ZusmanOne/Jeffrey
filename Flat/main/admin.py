from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *
from django.contrib.flatpages.models import FlatPage
from django.db import models


class FlatPageNewAdmin(FlatPageAdmin):
    save_on_top = True
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }


admin.site.unregister(FlatPage)
admin.site.register(FlatPage,  FlatPageNewAdmin)


# Register your models here.
