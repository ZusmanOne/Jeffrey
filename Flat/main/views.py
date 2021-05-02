from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required(login_url='accounts/login/')
def home(request):
    return render(request, 'index.html')


def header(request):
    return render(request, 'header.html')
# Create your views here.


@login_required(login_url='pages/')
def about(request):
    return render(request, 'flatpages/about.html')
