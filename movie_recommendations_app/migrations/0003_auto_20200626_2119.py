# Generated by Django 2.2.1 on 2020-06-26 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommendations_app', '0002_delete_myrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tvshows',
            old_name='title',
            new_name='name',
        ),
    ]
