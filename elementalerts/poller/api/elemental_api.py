import logging
import slumber
import time
from django.conf import settings

logger = logging.getLogger(__name__)

_url = settings.ELEMENTAL_MACHINES_URL
_access_token = settings.ACCESS_TOKEN

slumber = slumber.API(_url)

def get_user():
    """ 
    :return:                                                                                                T
    """
    users = slumber.api("users.json").get(access_token=_access_token)
    logger.debug(users)

def get_machine_list():
    return slumber.api("machines.json").get(access_token=_access_token)

def get_machine_details(machine_uuid):
    return slumber.api.machines("%s.json" % (machine_uuid)).get(access_token=_access_token, machine_uuid=machine_uuid)

def get_machine_alert_settings(machine_uuid):
    return slumber.api("alert_settings.json").get(access_token=_access_token, machine_uuid=machine_uuid)

def get_machine_samples(machine_uuid,last_sample_epoch=None):
    if not last_sample_epoch:
        last_sample_epoch = int(round(time.time())) - 60
    url_string=machine_uuid + '/samples.json'
    params = {'access_token':_access_token,'from':last_sample_epoch}
    return slumber.api.machines(url_string).get(**params)
    