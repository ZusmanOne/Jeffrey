from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import F




def index(request): #так же здесь реалтзовано пагинация
    news_objects = News.objects.all()
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    paginator = Paginator(news_objects, 3)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)
    # page_range = paginator.get_elided_page_range(on_ends = 2 )
    context = {'news': news_objects, 'title':'hello world','tag_list':tag_list, 'category_list': category_list, 'page_obj': page_objects}
    return render(request, 'news/index.html', context)


class NewsList(LoginRequiredMixin, ListView):  # отображение ленты новостей чрез CBV
    model = News
    template_name = 'news_list.html'
    context_object_name = 'my_news'
    queryset = News.objects.all().select_related('category')  # select_related для django debug toolbar

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_data'] = "Новостная лента"
        return context

#
# def category(request, category_id):
#     category = Category.objects.all()
#     news_category = News.objects.filter(category_id = category_id)
#     return render(request, 'news/category.html', {'category': category,'news_category': news_category})


class NewsCategory(LoginRequiredMixin, ListView):  # показывает новости по категориям
    model = News
    template_name = 'news/category.html'
    context_object_name = 'my_new'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])  # создается объект для модели
        # category,и через ключ category можно обращаться к полям модели category
        return context

    def get_queryset(self):
        category_news = News.objects.filter(category_id=self.kwargs['category_id']).select_related('category')
        '''метод select_related применяется для того что бы сократить количество sql запросов к связаной табоицу в модели News
        select_related применяется для Foreign Key для ManytpMany применятеся prefeatch'''
        return category_news


# @cache_page(30)  # кэширование для фунцкий
def news_object(request, news_id):
    single_news = get_object_or_404(News, pk=news_id)
    single_news.visits += 1
    single_news.save()
    return render(request, 'news/single_news.html', {'single_news': single_news})


class TagNews(ListView): # будет отображать теги
    model = News
    template_name = 'news/news_tag.html'
    context_object_name = 'news_tag'

    def get_queryset(self):
        tag_post = News.objects.filter(tag__slug= self.kwargs['slug'])
        return tag_post

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['tag'] = Tag.objects.all()
    #     return context


def add_news(request):  # контроллер для не связанной формы
    if request.method == 'POST':
        form = AddNews(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            news = News.objects.create(**form.cleaned_data)  # распковыввает слварь clened_data и присваивает
            # значения по ключам в этом словаре
            return redirect(news)
    else:
        form = AddNews()
    return render(request, 'news/add_news.html', {'form': form})


def add_category(request):  # контроллер для связанной формы
    if request.method == 'POST':
        form = AddCategory(request.POST)
        if form.is_valid():
            categories = form.save()
            return redirect('news')

    else:
        form = AddCategory()

    return render(request, 'news/add_category.html', {'form': form})


# class NewsCreate(CreateView): создание новости на основе CBV
#     model = News
#     fields = '__all__'
#     template_name = 'news/add_news.html'
# #
# class NewsDetail(DetailView): #отображение отдельной новости на основе CBV
#     model = News
#     template_name = 'news/single_news.html'
#     context_object_name = 'single_news'


class CategoryDelete(DeleteView):
    model = Category
    context_object_name = 'delete'
    success_url = reverse_lazy('news')


class NewsUpdate(UpdateView):
    model = News
    fields = '__all__'
    template_name = 'news/update_news.html'
    success_url = reverse_lazy('news')


# Регистрация пользователя
def register(request):
    if request.method == "POST":
        form = UserRegistrForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news')
        else:
            messages.error(request, 'Ошибка в региcтрации')
    else:
        form = UserRegistrForm()
    return render(request, 'news/register.html', {'form': form})


# контроллер для отправки эл. письма
def send_message(request):
    if request.method == "POST":
        form = SendForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['message'], 'bigmama93@mail.ru',
                      ['nikzubkov93@mail.ru', 'zusmanone1@gmail.com'],  fail_silently=False)
            if mail:
                messages.success(request, 'письмо отправлено')
                return redirect('send-mail')
            else:
                messages.error(request,'письмо не отправлено')
                return redirect('send-mail')
    else:
        form = SendForm()
    return render(request, 'news/send_mail.html', {'form': form})

