# Generated by Django 3.2.5 on 2021-07-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20210706_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='staff',
            field=models.ManyToManyField(to='backend.Staff'),
        ),
        migrations.AlterField(
            model_name='film',
            name='filmId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staffId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
