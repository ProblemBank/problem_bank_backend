# Generated by Django 3.2.3 on 2022-08-26 06:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('problembank', '0010_auto_20220826_1041'),
        ('Game2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='number',
        ),
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='room',
            name='problem_groups',
            field=models.ManyToManyField(to='problembank.ProblemGroup', verbose_name='گروه\u200cمسئله\u200cها'),
        ),
    ]
