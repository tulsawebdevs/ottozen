from django.shortcuts import render
from alerts.models import Commute
from users.forms import ProfileForm

def profile(request):
  
  if request.method == 'POST':
    data = {'user': request.user.id,
            'home_address': request.POST['home_address'],
            'home_city': request.POST['home_city'],
            'mobile_num': request.POST['mobile_num']}
    form = ProfileForm(data, instance=request.user.get_profile())
    print request.POST
    print form.is_valid()
    print form.errors
    if form.is_valid():
      print 'valid!'
      form.save()
  else:
    form = ProfileForm(instance=request.user.get_profile())

  commutes = Commute.objects.filter(user=request.user)
  profile = request.user.get_profile()

  return render(request, 'users/profile.html', {'commutes':commutes, 'profile': profile, 'form': form})
