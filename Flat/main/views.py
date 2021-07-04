from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.flatpages.models import FlatPage
from django.views.generic import ListView

@login_required(login_url='accounts/login/')
def home(request):
    return render(request, 'flatpages/index.html')


def header(request):
    return render(request, 'header.html')
# Create your views here.


@login_required(login_url='pages/')
def about(request):
    return render(request, 'flatpages/about.html')


class Search(ListView):
    template_name = 'search.html'
    context_object_name = 'content'
    def get_queryset(self):
        return FlatPage.objects.filter(content__icontains=self.request.GET.get('s'))