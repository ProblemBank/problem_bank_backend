# Generated by Django 3.2.3 on 2021-09-11 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problembank', '0003_auto_20210910_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judgeablesubmit',
            name='text_tmp1',
        ),
        migrations.RemoveField(
            model_name='judgeablesubmit',
            name='text_tmp2',
        ),
    ]