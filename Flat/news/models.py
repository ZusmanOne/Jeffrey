from django.db import models
from django.urls import reverse_lazy


class News(models.Model):
    title = models.CharField(help_text='введите заголовок для новости', max_length=150)
    content = models.TextField(help_text='введите содержание')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    photo = models.ImageField(help_text='добавьте фотографию(если требуется)', blank=True,
                              upload_to='photo/%Y/%m/%d') #создасться каталог в древовидном порядке где будут фотки
    file = models.FileField(help_text='добавьте файл(если требуется)', blank=True, upload_to='file/%Y/%m/%d')
    published = models.BooleanField(help_text='публиковать новость?', default=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ManyToManyField('Tag', null=True, blank=True )
    visits = models.IntegerField(default=0, verbose_name='Число просмотров')

    def __str__(self):
        return (self.title)

    def get_absolute_url(self):
        return reverse_lazy('news_object', kwargs={'news_id': self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-create_date']


class Category(models.Model):
    title_category = models.CharField( help_text='Введите название категории', max_length=100)

    def __str__(self):
        return(self.title_category)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={'category_id': self.pk})


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="название тега")
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse_lazy('tag-news', kwargs={'slug':self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']




# Create your models here.
