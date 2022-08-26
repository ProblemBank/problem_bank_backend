# Generated by Django 3.2.3 on 2022-08-26 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Game2', '0006_auto_20220827_0302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='team',
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='carrousel_lose_ratio_reward',
            field=models.IntegerField(default=0.5),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='carrousel_win_ratio_reward',
            field=models.IntegerField(default=1.5),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='easy_problem_reward',
            field=models.IntegerField(default=300),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='hard_problem_reward',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='last_room_cost',
            field=models.IntegerField(default=900),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='last_room_name',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='max_not_submitted_problems',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='max_room_number',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='max_time_to_play',
            field=models.IntegerField(default=14400),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='medium_problem_reward',
            field=models.IntegerField(default=400),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='problem_cost',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='so_hard_problem_reward',
            field=models.IntegerField(default=600),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL),
        ),
    ]
