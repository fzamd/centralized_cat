# Generated by Django 3.1.7 on 2021-03-14 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cat_backend', '0002_auto_20210314_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 14, 58, 27, 230064)),
        ),
        migrations.AlterField(
            model_name='record',
            name='isbn',
            field=models.CharField(max_length=13),
        ),
    ]
