from datetime import datetime, timedelta
import cronjobs

from alerts.models import Commute

@cronjobs.register
def send_alerts():
    now = datetime.now()
    buffer = timedelta(minutes=10)
    range_start = now - buffer
    range_end = now + buffer
    commutes = Commute.objects.filter(start_time__gte=range_start).filter(start_time__lte=range_end)
    for commute in commutes:
        print(commute)
    print "Look for traffic incidents along the route"
    print "Send text messages via twilio if you find any"

