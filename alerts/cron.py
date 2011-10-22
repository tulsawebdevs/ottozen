from urllib import quote
import requests
import json

import cronjobs

from alerts.models import Commute

@cronjobs.register
def send_alerts():
    commutes = Commute.objects.get_timely_commutes()
    for commute in commutes:
        directions_url = 'http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&sensor=false' % (quote(commute.start_address), quote(commute.end_address))
        r = requests.get(directions_url)
        print(r.content)
        #directions = json.load(r.content)
        #print(directions)
    print "Look for traffic incidents along the route"
    print "Get directions objects from Google Maps from start address to end address"
    print "For all the steps on all the routes from start address to end address, query the trif data for nearby incidents"
    print "Send text messages via twilio if you find any"
