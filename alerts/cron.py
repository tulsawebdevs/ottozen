import cronjobs

@cronjobs.register
def send_alerts():
    print "Loop over all commute records where start_time is soonish"
    print "Look for traffic incidents along the route"
    print "Send text messages via twilio if you find any"

