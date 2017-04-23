# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0003_auto_20170423_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='alert_type',
            field=models.CharField(default='TEMP_GOOD', max_length=10, choices=[('TEMP_LOW', 'Temperature is below safe range'), ('TEMP_HIGH', 'Temperature is above safe range'), ('TEMP_GOOD', 'Temperature back in safe range')]),
        ),
    ]
