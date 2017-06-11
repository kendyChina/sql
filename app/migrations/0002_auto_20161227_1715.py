# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-27 09:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='borrow',
            name='should_return',
            field=models.DateField(default=datetime.datetime(2017, 1, 26, 9, 15, 24, 118384, tzinfo=utc), verbose_name='应还日期'),
        ),
    ]
