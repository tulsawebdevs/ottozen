from datetime import datetime
import json
from math import sin, cos, asin, radians, sqrt
from urllib import quote

import cronjobs
from django.conf import settings
import requests
from twilio.rest import TwilioRestClient

from alerts.models import Commute, Alert


now = datetime.now()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

@cronjobs.register
def store_alerts():
    print("Checking TRIF for incidents")
    trif_url = 'http://trif.tulsawebdevs.org/alerts/incidents.json'
    incidents_response = requests.get(trif_url)
    incidents = json.loads(incidents_response.content)

    commutes = Commute.objects.get_timely_commutes()
    for commute in commutes:
        directions_url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&sensor=false' % (quote(commute.start_address), quote(commute.end_address))
        directions_response = requests.get(directions_url)
        directions = json.loads(directions_response.content)
        route = directions['routes'][0]
        prev_end_location = None
        for leg in route['legs']:
            for step in leg['steps']:
                start_location = step['start_location']
                end_location = step['end_location']
                for alert in incidents['alerts']:
                    distance_from_start = haversine(alert['geo']['longitude'], alert['geo']['latitude'], start_location['lng'], start_location['lat'])
                    distance_from_end = haversine(alert['geo']['longitude'], alert['geo']['latitude'], end_location['lng'], end_location['lat'])
                    if distance_from_start < 2 or distance_from_end < 2:
                        # distance_from_prev_end_to_current_start = haversine(prev_end_location['lng'], prev_end_location['lat'], start_location['lng'], start_location['lat'])
                        existing_alert = Alert.objects.filter(commute=commute, user=commute.user, created__year=now.year, created__month=now.month, created__day=now.day)
                        if not existing_alert:
                            text = 'Oh noes! %s %s' % (alert['description'], alert['title'])
                            alert = Alert.objects.create(commute=commute, user=commute.user,
                                                         sent=False, text=text)
                            alert.save()
                prev_end_location = end_location

@cronjobs.register
def send_alerts():
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    unsent_alerts = Alert.objects.filter(created__year=now.year, created__month=now.month, created__day=now.day, sent=False)
    for alert in unsent_alerts:
        try:
            client.sms.messages.create(
                to=alert.user.get_profile().mobile_num,
                from_='4155992671',
                body=alert.text)
            alert.sent=True
            alert.save()
        except:
            pass
        print("Sent text: %s" % alert.text)
