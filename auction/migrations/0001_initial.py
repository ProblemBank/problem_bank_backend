# Generated by Django 3.1 on 2021-08-23 21:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)], verbose_name='قیمت')),
                ('done_deal', models.BooleanField(default=False, null=True, verbose_name='خریداری شده')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Game.player')),
                ('problem_for_sell', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Game.problem', verbose_name='سوال برای فروش')),
            ],
        ),
    ]
