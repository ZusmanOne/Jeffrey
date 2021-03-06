from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from django.http import HttpResponse
from django.db.models import Q



def index(request):  # так же здесь реалтзовано пагинация
    news_objects = News.objects.all()
    category_list = Category.objects.all()
    tag_list = Tag.objects.all()
    paginator = Paginator(news_objects, 3)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)
    # page_range = paginator.get_elided_page_range(on_ends = 2 )
    """
    далее будет реалтзована форма для полписки на расслыки
    """
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscribe = form.save()
            if subscribe:
                messages.success(request, 'Вы успешно подписались на рассылку')
                return redirect('news')
            else:
                messages.error(request,'Произошла ошибка')
                return redirect('news')

    else:
        form = SubscribeForm()
    context = {
                'news': news_objects, 'title':'hello world', 'tag_list':tag_list, 'category_list': category_list,
               'page_obj': page_objects, 'form':form
    }
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
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])  # создается объект для модели
        # category,и через ключ category можно обращаться к полям модели category
        return context

    def get_queryset(self):
        category_news = News.objects.filter(category_id=self.kwargs['category_id']).select_related('category')
        '''метод select_related применяется для того что бы сократить количество sql запросов к связаной табоицу в модели News
        select_related применяется для Foreign Key для MaytpMany применятеся prefeatch'''
        return category_news


# @cache_page(30)  # кэширование для фунцкий
@login_required()
def news_object(request, news_id):
    single_news = get_object_or_404(News, pk=news_id)
    single_news.visits += 1
    single_news.save()
    comment_all = Comment.objects.filter(post=news_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False) # озгначает что пока модель не сохранять
            form.user = request.user #заполняется поле юзер из реквеста
            form.post = single_news # комментарий отобразится у той статьи которая открыта на сайте(взятому по ключу)
            form.save()
            return redirect(news_object, news_id)
    else:
        form = CommentForm()
    return render(request, 'news/single_news.html',
                  {'single_news': single_news, 'form': form, 'comment_all':comment_all})


class TagNews(LoginRequiredMixin, ListView): # будет отображать теги
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


@login_required()
@permission_required('news.add_news')
def add_news(request):  # контроллер для не связанной формы
    if request.method == 'POST':
        form = AddNews(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            news = News.objects.create(**form.cleaned_data)  # распковыввает слварь clened_data и присваивает
            # значения по ключам в этом словаре
            return redirect(news)
    else:
        form = AddNews()
    return render(request, 'news/add_news.html', {'form': form})


@login_required()
@permission_required('news.add_category')
def add_category(request):  # контроллер для связанной формы
    if request.method == 'POST':
        form = AddCategory(request.POST)
        if form.is_valid():
            categories = form.save()
            return redirect('news')

    else:
        form = AddCategory()

    return render(request, 'news/add_category.html', {'form': form})

# class CategoryCreate(CreateView):
#     model = Category
#     form_class = AddCategory
#     template_name = 'news/add_category.html'
#     success_url = reverse_lazy('category')


# class NewsCreate(CreateView): создание новости на основе CBV
#     model = News
#     fields = '__all__'
#     template_name = 'news/add_news.html'
# #
# class NewsDetail(DetailView): #отображение отдельной новости на основе CBV
#     model = News
#     template_name = 'news/single_news.html'
#     context_object_name = 'single_news'


class CategoryDelete(LoginRequiredMixin,DeleteView):
    permission_required = 'news.delete_category'
    model = Category
    context_object_name = 'delete'
    success_url = reverse_lazy('news')


class NewsUpdate(LoginRequiredMixin,UpdateView):
    permission_required = 'news.update_news'
    model = News
    fields = ['title','content', 'category', 'published', 'tag',  'photo']
    template_name = 'news/update_news.html'
    success_url = reverse_lazy('news')


class NewsDelete(DeleteView):
    permission_required = 'news.delete_news'
    model = News
    context_object_name = "delete_news"
    success_url = reverse_lazy('news')
    template_name = 'news/news_delete.html'


# Регистрация пользователя
# def register(request):
#     if request.method == "POST":
#         form = UserRegistrForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('news')
#         else:
#             messages.error(request, 'Ошибка в региcтрации')
#     else:
#         form = UserRegistrForm()
#     return render(request, 'news/register.html', {'form': form})


# контроллер для отправки эл. письма
@login_required()
def send_message(request): #данная функция отправляет форму с электронным письмом
    if request.method == "POST":
        form = SendForm(request.POST)
        if form.is_valid():
            recipient_list = Subscribe.objects.all()
            subject = form.cleaned_data['subject']
            from_email = "jeffreyscoffee@gmail.com"
            text_content = form.cleaned_data['message']
            msg = EmailMultiAlternatives(subject, text_content, from_email, bcc=recipient_list)
            msg.send()
            # mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['message'], 'bigmama93@mail.ru',
            #           bcc= recipient_list,  fail_silently=False)
            if msg:
                messages.success(request, 'Письмо отправлено')
                return redirect('send-mail')
            else:
                messages.error(request,'Ошибка, письмо не отправлено')
                return redirect('send-mail')
    else:
        form = SendForm()

    return render(request, 'news/send_mail.html', {'form': form})


def send_mail_post(request):
    subject = 'Новости Jeffreys'
    from_email = "jeffreyscoffee@gmail.com"
    to = Subscribe.objects.all()
    text_content = 'У нас для вас новости https://jeffreysinfo.ru/news/'
    msg = EmailMultiAlternatives(subject,text_content,from_email, bcc=to)
    msg.send()


@receiver(post_save, sender = News) # применяется сигнал по которому после добавления поста будет отправлено
# письмо из ф-ии send+mail
def create_post(instance,  created, **kwargs):
    if created:
        # News.objects.get_or_create(pk=instance.pk) эта строчка выполнится если увидит что  создался еще раз
        # объект класса News (тоесть она  попытается создать еще раз этот объект)
        send_mail_post(instance) # здесь выполнится функция по отправке почты если был создан объект класса News
        print('почта отправлена')


# class SubscribeView(CreateView):
#     model = Subscribe
#     form_class = SubscribeForm
#     template_name = 'news/index.html' #выяснить как выводить ошибку в случае одинаковой почты
#     success_url = reverse_lazy('news')


class SearchBlog(ListView): #Поиск новостей в блоге по навзанию и содержанию
    template_name = 'news/search_blog.html'
    context_object_name = 'search_blog'

    def get_queryset(self):
        search_blog = News.objects.filter(Q(title__icontains=self.request.GET.get('b'))
                                          | Q(content__icontains=self.request.GET.get('b')))
        return (search_blog)