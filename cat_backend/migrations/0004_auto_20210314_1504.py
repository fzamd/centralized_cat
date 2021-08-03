# Generated by Django 3.1.7 on 2021-03-14 15:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat_backend', '0003_auto_20210314_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 15, 4, 1, 132898)),
        ),
        migrations.AlterField(
            model_name='record',
            name='edition',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='publish_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
