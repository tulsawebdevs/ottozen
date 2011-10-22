import cronjobs

from alerts.models import Commute

@cronjobs.register
def send_alerts():
    commutes = Commute.objects.get_timely_commutes()
    for commute in commutes:
        print(commute)
    print "Look for traffic incidents along the route"
    print "Get directions objects from Google Maps from start address to end address"
    print "For all the steps on all the routes from start address to end address, query the trif data for nearby incidents"
    print "Send text messages via twilio if you find any"
