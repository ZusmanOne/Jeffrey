from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [

    path('', index, name='news'),
    # path('subscribe/', SubscribeView.as_view(), name = 'subscribe'), #контр-лер не рааботает по корневому
    # маршруту нужно выяснить почему
    # path('', NewsList.as_view(), name = 'news'),
    # path('category/<int:category_id>/', category, name='category'),
    path('category/<int:category_id>/', NewsCategory.as_view(), name = 'category'),
    path('<int:news_id>/', news_object, name='news_object'),
    path('add_news/', add_news, name='add_news'),
    path('add_category/', add_category, name='add_category'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='delete-category'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete-news'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='update_news'),
    # path('registration/', register, name='register'),
    path('send_mail/', send_message, name='send-mail'),
    path('tag/<str:slug>', TagNews.as_view(), name = 'tag-news'),
    path('search_news/', SearchBlog.as_view(), name = 'search_blog')


]