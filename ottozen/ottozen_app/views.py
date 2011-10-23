from django.shortcuts import render
from django.views.generic.create_update import create_object

from forms import ProfileForm
from models import Route, UserProfile

def home(request):
  return render(request, 'home.html')# Create your views here.

def signup(request):
  return render(request, 'signup.html')
  
def myroutes(request):
  return render(request, 'myroutes.html')

def old_add(request):
    return create_object(request, model=Route, login_required=True,
        post_save_redirect='/commutes/add')

def old_profile(request):
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
