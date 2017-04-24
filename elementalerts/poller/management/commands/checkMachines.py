from django.core.management.base import BaseCommand
from ...models import Machine, Alert
from ...api.elemental_api import get_machine_alert_settings, get_machine_samples, get_user, get_machine_details
from ...api.twilio_api import make_voice_call
import logging
from decimal import *
from django.utils import timezone

HIGH_LIMIT  = 'high_limit'
LOW_LIMIT = 'low_limit'
TEMP_VARIABLE = 'tempextcal'

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check all active machines for alerts'

    def handle(self, *args, **options):
        # Query all active machines from locally stored list
        for machine in Machine.objects.all():
            check_machine(machine)

def check_sample(temp, alert_settings):
    """Return boolean for whether sample is in acceptable range.

    Positional arguments:
    temp - temperature to check
    alert_settings -- dict of settings to check against
    
    :return: TEMP_GOOD, TEMP_LOW, or TEMP_HIGH 
    """

    # If no range settings, we default to true
    ret = Alert.ALERT_TYPE_TEMP_GOOD;
    
    # Check against upper limit only if one exists
    if alert_settings[HIGH_LIMIT] and temp > Decimal(alert_settings[HIGH_LIMIT]):
        ret = Alert.ALERT_TYPE_TEMP_HIGH
    # Check against lower limit only if one exists
    elif alert_settings[LOW_LIMIT] and temp < Decimal(alert_settings[LOW_LIMIT]):
        ret = Alert.ALERT_TYPE_TEMP_LOW 
    #logger.debug("  Temp %s between %s and %s: %s" % (temp, alert_settings[LOW_LIMIT], alert_settings[HIGH_LIMIT], ret))

    return ret


def raise_alert(machine, current_state, current_temp, alert_settings):
    machine_details = get_machine_details(machine.machine_uuid)
    user_info = get_user()
    
    if current_state == Alert.ALERT_TYPE_TEMP_GOOD:
        alert_message = "This message is from Elemental Machines. The temperature of device %s at %s is back in acceptable range. The current temperature is %s degrees celcius." % \
                        (machine_details["name"], machine_details["location"], current_temp)
    elif current_state == Alert.ALERT_TYPE_TEMP_LOW: 
        alert_message = "This message is from Elemental Machines. The temperature of device %s at %s has fallen below the acceptable range. The current temperature is %s degrees celcius." % \
                        (machine_details["name"], machine_details["location"], current_temp)
    elif current_state == Alert.ALERT_TYPE_TEMP_HIGH: 
        alert_message = "This message is from Elemental Machines. The temperature of device %s at %s has gone above the acceptable range. The current temperature is %s degrees celcius." % \
                        (machine_details["name"], machine_details["location"], current_temp)
    
    logger.info("Message sent to user on %s: %s" % (user_info['mobile'],alert_message))
    
    """ Take appropriate action if machine state has changed """
    alert = Alert(
        machine=machine,
        alert_date= timezone.now(),
        alert_type=current_state,
        message=alert_message
        )
    alert.save()
    make_voice_call(user_info, alert)


def check_machine(machine):
    """ Examine recent sample from a given machine """

    # Get all alert settings for the machine
    alert_settings = [x for x in get_machine_alert_settings(machine.machine_uuid) if x['sample_var'] == TEMP_VARIABLE] 

    
    if not alert_settings:
        logger.error("No alert settings found for machine %s" %(machine));
    else:
        alert_settings = alert_settings[0]

    logger.debug("Machine %s range: Min %s - Max %s" % (machine.machine_uuid, alert_settings[LOW_LIMIT], alert_settings[HIGH_LIMIT]))

    if not alert_settings['enabled']:
        # alert disabled
        return
    
    # Get last known state, for comparison
    last_sample_epoch = machine.last_sample_epoch
    last_sample_temp = machine.last_sample_temp 
    last_state = check_sample(last_sample_temp, alert_settings)

    machine_samples = get_machine_samples(machine.machine_uuid,last_sample_epoch + 1 )
    for sample in machine_samples:
        current_temp = Decimal(sample[TEMP_VARIABLE])
        current_state = check_sample(current_temp, alert_settings)

        # Is we have gone out of range (or back in) create an alert
        if current_state != last_state and last_state:
            raise_alert(machine, current_state, current_temp, alert_settings)
        last_sample_epoch = sample['sample_epoch']
        last_sample_temp = current_temp
        last_state = current_state

    # Persist the latest state of each machine for the next run of this function
    machine.last_sample_epoch = last_sample_epoch
    machine.last_sample_temp = last_sample_temp
    machine.save()