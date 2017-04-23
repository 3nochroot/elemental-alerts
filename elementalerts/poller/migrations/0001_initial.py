# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 20:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alert_date', models.DateTimeField(verbose_name='date published')),
                ('alert_type', models.CharField(choices=[('TEMP_BAD', 'Temperature out of range'), ('TEMP_GOOD', 'Temperature back in safe range')], default='TEMP_BAD', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_uuid', models.CharField(max_length=36)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='alert',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poller.Machine'),
        ),
    ]