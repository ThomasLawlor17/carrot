# Generated by Django 4.0.4 on 2022-05-27 15:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_run_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gear',
            name='image',
            field=models.CharField(default='https://i.imgur.com/iOWhgv1.png', max_length=200),
        ),
        migrations.AlterField(
            model_name='run',
            name='date',
            field=models.DateField(default=datetime.date(2022, 5, 27)),
        ),
        migrations.AlterField(
            model_name='run',
            name='image',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='name',
            field=models.CharField(default='Afternoon Run', max_length=50),
        ),
    ]