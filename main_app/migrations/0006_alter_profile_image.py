# Generated by Django 4.0.4 on 2022-05-23 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.CharField(default='https://i.imgur.com/G4NNtuW.png', max_length=100),
        ),
    ]