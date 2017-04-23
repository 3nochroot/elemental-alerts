# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Machine
from .models import Alert

# Register your models here.
admin.site.register(Machine)
admin.site.register(Alert)