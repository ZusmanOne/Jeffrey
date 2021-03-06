"""Flat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
import main.views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.conf import settings

from django.views.decorators.cache import cache_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('', main.views.home, name='Home'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('header/', main.views.header, name='header'),
    path('/', include('main.urls')),
    path('news/', include('news.urls')),

]

if settings.DEBUG:
    # import debug_toolbar
    #
    # urlpatterns = [
    #                     path('__debug__/', include(debug_toolbar.urls)), # добавили модуль django debug toolbar
    #                 ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  # что бы загруженные файлы
    # можно было просматривать на сайте в режиме отладки, создается этот маршрут с помощью ф-ии static()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
    ]