# Generated by Django 3.2.5 on 2021-07-12 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20210712_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
