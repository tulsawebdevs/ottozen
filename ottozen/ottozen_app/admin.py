from django.contrib import admin
from models import Alert, Point, Route, RoutePoint, UserProfile

admin.site.register(Alert)
admin.site.register(Point)
admin.site.register(Route)
admin.site.register(RoutePoint)
admin.site.register(UserProfile)
