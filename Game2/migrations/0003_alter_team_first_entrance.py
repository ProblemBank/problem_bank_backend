# Generated by Django 3.2.3 on 2022-08-26 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game2', '0002_auto_20220826_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='first_entrance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
