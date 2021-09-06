# Generated by Django 3.2.3 on 2021-09-06 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problembank', '0004_alter_problem_problem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descriptiveproblem',
            name='answer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='problem', to='problembank.descriptiveanswer', verbose_name='پاسخ صحیح'),
        ),
    ]
