# Generated by Django 3.2.5 on 2021-07-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_genre_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(to='backend.Genre'),
        ),
    ]
