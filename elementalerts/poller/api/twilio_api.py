import logging
import urllib
from django.conf import settings

logger = logging.getLogger(__name__)

from twilio.rest import Client
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token  = settings.TWILIO_AUTH_TOKEN
twilio_client = Client(account_sid, auth_token)

def make_voice_call(alert):
    # Construct twilio url
    echo_url = 'http://twimlets.com/echo?Twiml=' + \
               urllib.quote('<Response><Say>' + alert.message  + '</Say></Response>')
    
    # Use Twilio client to make a voice call    
    call = twilio_client.calls.create(
        url=echo_url,
        to="+16176942008",   #message from user
        from_=settings.TWILIO_NUMBER)
    logger.info("Twilio call from %s, sid=%s"  % (settings.TWILIO_NUMBER,call.sid))
