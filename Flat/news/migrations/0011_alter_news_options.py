# Generated by Django 3.2.5 on 2021-08-05 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20210802_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-update_date'], 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
    ]