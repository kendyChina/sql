# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 10:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bname', models.CharField(max_length=30)),
                ('bcount', models.IntegerField()),
                ('bposition', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_time', models.DateField(default=django.utils.timezone.now, verbose_name='借书日期')),
                ('should_return', models.DateField(default=datetime.datetime(2017, 1, 19, 10, 26, 2, 766976, tzinfo=utc), verbose_name='应还日期')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dname', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=10)),
                ('sage', models.IntegerField()),
                ('password', models.CharField(max_length=10)),
                ('sdepartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='borrow',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Student'),
        ),
        migrations.AddField(
            model_name='book',
            name='btype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Type'),
        ),
    ]
