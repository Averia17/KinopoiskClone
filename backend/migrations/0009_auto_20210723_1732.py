# Generated by Django 3.2.5 on 2021-07-23 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20210714_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='film',
            name='year',
            field=models.CharField(max_length=9),
        ),
    ]
