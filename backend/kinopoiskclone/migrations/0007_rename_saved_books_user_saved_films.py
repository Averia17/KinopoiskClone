# Generated by Django 3.2.5 on 2021-12-09 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kinopoiskclone', '0006_auto_20211206_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='saved_books',
            new_name='saved_films',
        ),
    ]