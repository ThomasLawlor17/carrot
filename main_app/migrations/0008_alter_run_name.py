# Generated by Django 4.0.4 on 2022-05-24 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_run_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='name',
            field=models.CharField(default='Morning Run', max_length=50),
        ),
    ]
