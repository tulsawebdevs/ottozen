from django.shortcuts import render
from alerts.models import Commute

def profile(request):
    commutes = Commute.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'commutes':commutes})
