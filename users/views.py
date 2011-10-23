from django.shortcuts import render
from alerts.models import Commute
from users.forms import ProfileForm
from users.models import UserProfile

def profile(request):
  
  try:
    profile = request.user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile.objects.create(user=request.user)
  if request.method == 'POST':
    data = {'user': request.user.id,
            'home_address': request.POST['home_address'],
            'home_city': request.POST['home_city'],
            'mobile_num': request.POST['mobile_num']}
    form = ProfileForm(data, instance=profile)
    print request.POST
    print form.is_valid()
    print form.errors
    if form.is_valid():
      print 'valid!'
      form.save()
  else:
    form = ProfileForm(instance=profile)

  commutes = Commute.objects.filter(user=request.user)
  profile = request.user.get_profile()

  return render(request, 'users/profile.html', {'commutes':commutes, 'profile': profile, 'form': form})
