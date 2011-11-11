import re

from django.conf import settings
from twilio.rest import TwilioRestClient

CONFIRM_TEXT = "Please reply to this text to confirm your mobile number for OttoZen."
THANK_YOU_TEXT = "Thanks. OttoZen has verified your mobile number."

def to_e164(mobile_num):
    non_decimal = re.compile(r'[^\d]+')
    mobile_num = non_decimal.sub('', mobile_num)
    if not mobile_num[0] == '1':
        mobile_num = '1'+mobile_num
    return mobile_num

def send_confirmation_text(user, mobile_num):
    # invoke twilio text message to mobile_num
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.sms.messages.create(
            to=mobile_num,
            from_=settings.TWILIO_NUMBER,
            body=CONFIRM_TEXT)
    except:
        pass
