from django.urls import path
from .views import Search


urlpatterns = [
    path('search/', Search.as_view(), name='search'),
    # path('', get_text, name='text')
]
