
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.create_update import create_object
from django.views.decorators.csrf import csrf_exempt

from forms import LoginForm, ProfileForm
from models import Point, Route, RoutePoint, UserProfile
from utils import to_e164, send_confirmation_text, THANK_YOU_TEXT

def home(request):
  return render(request, 'home.html')# Create your views here.

def myroutes(request):
  try:
    profile = request.user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile.objects.create(user=request.user)

  routes = Route.objects.filter(user=request.user)

  profile = request.user.get_profile()
  print profile.mobile_num

  for route in routes:
    print route.waypoints

    for waypoint in route.waypoints.order_by('routepoint__sequence').all():
      print waypoint

  return render(request, 'myroutes.html', {'mobile_num': profile.mobile_num, 'routes': routes})

def phone(request):
  return render(request, 'phone.html')

def do_login(request):
  form = LoginForm(request.REQUEST)
  if form.is_valid():
    user = None
    ident = form.cleaned_data['dummy_name']
    password = form.cleaned_data['password']

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
    else:
      a_user = authenticate(username=user.username, password=password)
      if a_user is not None:
        if a_user.is_active:
          login(request, a_user)
          message = "OK"
          status = 200
        else:
          message = "Your account is disabled"
          status = 401
      else:
        message = "Wrong password for %s" % ident
        status = 401
  else:
    message = 'Please enter all fields'
    status = 401

  return HttpResponse(message, status=status)

def do_logout(request):
  logout(request)
  return redirect('home')

def old_add(request):
    return create_object(request, model=Route, login_required=True,
        post_save_redirect='/commutes/add')


def account(request, email):
    user = None
    if email:
        user = get_object_or_404(User, username=email)
    if request.method == 'POST':
        mobile_num = to_e164(request.POST['mobile_num'])
        if not user:
            user = User.objects.create(username=request.POST['email'], password=request.POST['password'], email=request.POST['email'])
            UserProfile.objects.create(user=user)
            send_confirmation_text(user, mobile_num)
        profile_data = {'mobile_num': mobile_num}
        UserProfile.objects.filter(user=user).update(**profile_data)
    profile = user.get_profile() if user else None
    return render(request, 'account.html', {'user': user, 'profile': profile})

@csrf_exempt
def account_sms_confirm(request):
    mobile_num = to_e164(request.POST['From'])
    profile = UserProfile.objects.get(mobile_num=mobile_num)
    profile.mobile_confirmed = True
    profile.save()
    return render(request, 'account_sms_confirm.xml', {'Sms': THANK_YOU_TEXT}, content_type='application/xml')

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
