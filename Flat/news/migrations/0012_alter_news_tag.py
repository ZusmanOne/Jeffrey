# Generated by Django 3.2.5 on 2021-08-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_news_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tag',
            field=models.ManyToManyField(blank=True, to='news.Tag'),
        ),
    ]