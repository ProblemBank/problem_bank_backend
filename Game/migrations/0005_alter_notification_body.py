# Generated by Django 3.2.3 on 2021-09-09 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0004_auto_20210909_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='body',
            field=models.TextField(verbose_name='متن'),
        ),
    ]
