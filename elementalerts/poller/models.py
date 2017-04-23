# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models


class Machine(models.Model):
    machine_uuid = models.CharField(max_length=36)
    last_sample_epoch = models.IntegerField(blank=True,null=True)
    last_sample_temp = models.DecimalField(blank=True,null=True,max_digits=10, decimal_places=4)
    def __unicode__( self ):
           return self.machine_uuid
    @property
    def last_sample_date(self):
        if self.last_sample_epoch:
            return datetime.datetime.fromtimestamp(self.last_sample_epoch)
        else:
            return None
    

class Alert(models.Model):
    ALERT_TYPE_TEMP_LOW = 'TEMP_LOW'
    ALERT_TYPE_TEMP_HIGH = 'TEMP_HIGH'
    ALERT_TYPE_TEMP_GOOD = 'TEMP_GOOD'
    ALERT_TYPE_CHOICES = (
        (ALERT_TYPE_TEMP_LOW,  'Temperature is below safe range'),
        (ALERT_TYPE_TEMP_HIGH,  'Temperature is above safe range'),
        (ALERT_TYPE_TEMP_GOOD, 'Temperature back in safe range')
    )

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    alert_date = models.DateTimeField('date published')
    alert_type = models.CharField(
       max_length=10,
       choices=ALERT_TYPE_CHOICES,
       default=ALERT_TYPE_TEMP_GOOD,
   )    
    message = models.TextField(blank=True,null=True)
    def __unicode__( self ):
        return "{0} {1} {2}".format( self.machine.machine_uuid, self.alert_date, self.alert_type )

