from django.shortcuts import render
from alerts.models import Commute

def profile(request):
    commutes = Commute.objects.filter(user=request.user)
    profile = request.user.get_profile()
    return render(request, 'users/profile.html', {'commutes':commutes, 'profile': profile})
