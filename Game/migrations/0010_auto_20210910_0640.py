# Generated by Django 3.2.3 on 2021-09-10 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0009_auto_20210910_0629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkableobject',
            name='image',
        ),
        migrations.RemoveField(
            model_name='famousperson',
            name='is_fake',
        ),
        migrations.AddField(
            model_name='checkableobject',
            name='is_fake',
            field=models.BooleanField(default=False, verbose_name='آیا تقلبی است؟'),
        ),
    ]
