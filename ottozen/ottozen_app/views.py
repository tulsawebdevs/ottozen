from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.create_update import create_object

from forms import LoginForm, ProfileForm
from models import Route, UserProfile

def home(request):
  return render(request, 'home.html')# Create your views here.

def signup(request):
  return render(request, 'signup.html')
  
def myroutes(request):
  try:
    profile = request.user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile.objects.create(user=request.user)

  #commutes = Commute.objects.filter(user=request.user)
  profile = request.user.get_profile()
  print profile.mobile_num
  return render(request, 'myroutes.html', {'mobile_num': profile.mobile_num})
    
def phone(request):
  return render(request, 'phone.html')

def login(request):
  form = LoginForm(request.REQUEST)
  if form.is_valid():
    user = None
    ident = form.cleaned_data['dummy_name']
    
    if not user:
      try:
        user = User.objects.get(email=ident)
      except User.DoesNotExist:
        pass
    
    if not user:
      try:
        user = UserProfile.objects.get(mobile_num=ident).user
      except UserProfile.DoesNotExist:
        pass
    
    if not user:
      try:
        user = User.objects.get(username=ident)
      except User.DoesNotExist:
        pass
    
    if not user:
      message = "We couldn't find a matching mobile number or email"
      status = 401
    elif user.check_password(form.cleaned_data['password']):
      message = "OK"
      status = 200
    else:
      message = "Wrong password for %s" % ident
      status = 401
  else:
    message = 'Please enter all fields'
    status = 401
    
  return HttpResponse(message, status=status)

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
