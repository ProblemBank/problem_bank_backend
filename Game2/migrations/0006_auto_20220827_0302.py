# Generated by Django 3.2.3 on 2022-08-26 22:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problembank', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Game2', '0005_auto_20220827_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='group_problems',
            field=models.ManyToManyField(related_name='team', to='problembank.ProblemGroup'),
        ),
        migrations.AlterField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(related_name='team', to=settings.AUTH_USER_MODEL, verbose_name='اعضا'),
        ),
    ]
