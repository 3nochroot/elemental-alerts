import logging
import re
import urllib
from django.conf import settings

logger = logging.getLogger(__name__)

from twilio.rest import Client
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token  = settings.TWILIO_AUTH_TOKEN
twilio_client = Client(account_sid, auth_token)


def convert_to_e164(phone_number_string):
    #phone_number_string = "617-694-2008" # Hard code my own phone number
    digits =  re.sub('[^0-9]+', '', phone_number_string)
    if digits.__len__() == 10:
        digits = "+1" + digits
    elif digits.__len__() > 10:
        digits = "+" + digits
        
    return digits
        


def make_voice_call(user_info, alert):
    phone_number_string = user_info['mobile']
    phone_number = convert_to_e164(phone_number_string)
    
    # Construct twilio echo url
    # The echo endpoint allows us to generate a URL with our message text without actually serving the page from our app
    echo_url = 'http://twimlets.com/echo?Twiml=' + \
               urllib.quote('<Response><Say>' + alert.message  + '</Say></Response>')
    
    # Use Twilio client to make a voice call    
    call = twilio_client.calls.create(
        url=echo_url,
        to=phone_number,   #message from user
        from_=settings.TWILIO_NUMBER,
        machine_detection="DetectMessageEnd")
    logger.info("Twilio call from %s to %s, sid=%s"  % (settings.TWILIO_NUMBER,phone_number, call.sid))
