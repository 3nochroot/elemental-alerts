from django.shortcuts import render
from .models import Machine, Alert
from django.template import loader

def index(request):
    machine_list = Machine.objects.order_by('machine_uuid')
    alert_list = Alert.objects.order_by('-alert_date')[:20]
    context = {'machine_list': machine_list, 'alert_list': alert_list}

    return render(request, 'machine/index.html', context)