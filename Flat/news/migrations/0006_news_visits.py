# Generated by Django 3.2.5 on 2021-07-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_tag_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='visits',
            field=models.IntegerField(default=0, verbose_name='Число просмотров'),
        ),
    ]
