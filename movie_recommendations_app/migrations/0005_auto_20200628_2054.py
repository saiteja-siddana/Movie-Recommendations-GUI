# Generated by Django 2.2.1 on 2020-06-28 15:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendations_app', '0004_auto_20200626_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myrating',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]
