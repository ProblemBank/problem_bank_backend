# Generated by Django 3.2.3 on 2021-09-06 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0021_alter_baseanswer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseanswer',
            name='status',
            field=models.CharField(choices=[('RECEIVED', 'Received'), ('DELIVERED', 'Delivered'), ('SCORED', 'Scored')], default='RECEIVED', max_length=10, verbose_name='وضعیت'),
        ),
    ]
