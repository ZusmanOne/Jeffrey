from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.flatpages.models import FlatPage
from django.views.generic import ListView
from news.models import *
from django.db.models import Q
from itertools import chain


@login_required(login_url='accounts/login/')
def home(request):
    return render(request, 'flatpages/index.html')


def header(request):
    return render(request, 'header.html')
# Create your views here.


# def get_text(request):
#     context = 'hello world'
#     return render(request, 'flatpages/index.html', {'context':context})

@login_required(login_url='pages/')
def about(request):
    return render(request, 'flatpages/about.html')


class Search(ListView):
    template_name = 'search.html'
    context_object_name = 'content'
    # return render(request, 'search.html')
    def get_queryset(self):
        search_flat = FlatPage.objects.filter(content__icontains=self.request.GET.get('s'))
        search_news = News.objects.filter(content__icontains=self.request.GET.get('s'))
        search_list = list(chain(search_flat,search_news))
        return (search_list)
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


