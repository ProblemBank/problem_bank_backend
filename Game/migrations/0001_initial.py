# Generated by Django 3.2.3 on 2021-09-08 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('start_date', models.DateTimeField(verbose_name='تاریخ شروع')),
                ('finish_date', models.DateTimeField(verbose_name='تاریخ پایان')),
                ('maximum_number_of_received_problem', models.IntegerField(default=2, verbose_name='حداکثر تعداد سوالاتی که بازیکن در یک لحظه می\u200cتواند داشته باشد')),
                ('maximum_number_of_received_problem_per_subject', models.IntegerField(default=6, verbose_name='حداکثر تعداد سوالاتی که یک بازیکن در کل مسابقه از یک مبحث می\u200cتواند داشته باشد')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام بازیکن')),
                ('score', models.IntegerField(default=0, verbose_name='امتیاز')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Game.game', verbose_name='بازی')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='کاربر(ان)')),
            ],
        ),
    ]
