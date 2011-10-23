from django.contrib import admin
from models import Alert, Point, Route, RoutePoints, UserProfile

admin.site.register(Alert)
admin.site.register(Point)
admin.site.register(Route)
admin.site.register(RoutePoints)
admin.site.register(UserProfile)

