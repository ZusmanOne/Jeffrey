from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required(login_url='accounts/login/')
def home(request):
    return render(request, 'index.html')



# Create your views here.
