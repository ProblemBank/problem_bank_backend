# Generated by Django 3.2.3 on 2021-09-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='maximum_number_of_received_problem_per_subject',
            field=models.IntegerField(default=6, verbose_name='حداکثر تعداد سوالاتی که یک بازیکن در کل مسابقه از یک دسته می\u200cتواند داشته باشد'),
        ),
    ]
