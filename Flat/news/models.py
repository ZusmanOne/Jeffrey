from django.db import models

class news(models.Model):
    title = models.CharField(help_text='введите заголовок для новости', max_length=150)
    content = models.TextField(help_text='введите содержание')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    photo = models.ImageField(help_text='добавьте фотографию(если требуется)', blank=True,
                              upload_to='photo/%Y/%m/%d') #создаться каталог в древовидном порядке где будут фотки
    file = models.FileField(help_text='добавьте файл(если требуется)', blank=True, upload_to='file/%Y/%m/%d')
    published = models.BooleanField(help_text='публиковать новость?', default=True)

# Create your models here.
