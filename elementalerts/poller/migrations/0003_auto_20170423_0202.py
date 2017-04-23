# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poller', '0002_auto_20170422_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='active',
        ),
        migrations.AddField(
            model_name='alert',
            name='message',
            field=models.TextField(null=True, blank=True),
        ),
    ]
