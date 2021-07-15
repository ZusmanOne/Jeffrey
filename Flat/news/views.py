from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.views.generic import ListView,DeleteView, CreateView,UpdateView,DetailView
from django.urls import reverse_lazy

# def index(request):
#     news_objects = News.objects.all()
#     category_list = Category.objects.all()
#     context = {'news': news_objects, 'title':'hello world', 'category_list': category_list}
#     return render(request, 'news/index.html', context)


class NewsList(ListView): # отображение ленты новостей чрез CBV
    model = News
    template_name = 'news_list.html'
    context_object_name = 'my_news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_data'] = "Новостная лента"
        return context


# def category(request, category_id):
#     category = Category.objects.all()
#     news_category = News.objects.filter(category_id = category_id)
#     return render(request, 'news/category.html', {'category': category,'news_category': news_category})


class NewsCategory(ListView): # показывает новости по категориям
    model = News
    template_name = 'news/category.html'
    context_object_name = 'my_new'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk = self.kwargs['category_id']) # создается объект для модели
        # category,и через ключ category можно обращаться к полям модели category
        return context

    def get_queryset(self):
        category_news = News.objects.filter(category_id = self.kwargs['category_id'])
        return category_news


def news_object(request, news_id):
    single_news = get_object_or_404(News, pk= news_id)
    return render(request, 'news/single_news.html', {'single_news':single_news})


def add_news(request): # контроллер для не связанной формы
    if request.method == 'POST':
        form = AddNews(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            news = News.objects.create(**form.cleaned_data) # распковыввает слварь clened_data и присваивает
            # значения по ключам в этом словаре
            return redirect(news)
    else:
        form = AddNews()
    return render(request, 'news/add_news.html', {'form': form})


def add_category(request): # контроллер для связанной формы
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
# class NewsDetal(DetailView): #отображение отдельной новости на основе CBV
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

