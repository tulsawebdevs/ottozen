from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.create_update import create_object
from django.views.decorators.csrf import csrf_exempt

from forms import LoginForm, ProfileForm
from models import Route, UserProfile
from utils import to_e164, send_confirmation_text, THANK_YOU_TEXT

def home(request):
    routes = None
    if not request.user.is_anonymous():
        routes = Route.objects.filter(user=request.user)
    return render(request, 'home.html', {'routes': routes})

def myroutes(request):
  try:
    profile = request.user.get_profile()
  except UserProfile.DoesNotExist:
    profile = UserProfile.objects.create(user=request.user)

  routes = Route.objects.filter(user=request.user)

  return render(request, 'myroutes.html',
    {'mobile_num': profile.mobile_num, 'routes': routes})

def phone(request):
  return render(request, 'phone.html')

def login(request):
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
      a_user = auth.authenticate(username=user.username, password=password)
      if a_user is not None:
        if a_user.is_active:
          auth.login(request, a_user)
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

def logout(request):
  auth.logout(request)
  return redirect('home')

def old_add(request):
    return create_object(request, model=Route, login_required=True,
        post_save_redirect='/commutes/add')

def route(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated():
            # store the route in the database for the user
            r = Route(user=request.user, json=request.POST['route_json'])
            r.save()
            return redirect('myroutes')
        else:
            # store the route in session
            # will store route in database for the user after
            # we create the user
            request.session['route_json'] = request.POST['route_json']
            return redirect('account')
    else:
        return redirect('home')

def account(request, email):
    user = None
    if email:
        user = get_object_or_404(User, username=email)
    if request.method == 'POST':
        email = request.POST['email']
        mobile_num = to_e164(request.POST['mobile_num'])
        password = request.POST['password']
        if not user:
            if password == request.POST['confirm']:
                user = User.objects.create(username=email, email=email)
                user.set_password(password)
                user.save()
                UserProfile.objects.create(user=user).save()
                send_confirmation_text(user, mobile_num)
                user = auth.authenticate(username=user.username, password=password)
                auth.login(request, user)
                try:
                  route_json = request.session['route_json']
                except IndexError:
                  pass
                else:
                  r = Route(user=request.user, json=route_json, start_time=request.POST['start_time'])
                  r.save()
        profile_data = {'mobile_num': mobile_num}
        UserProfile.objects.filter(user=user).update(**profile_data)
        return redirect('myroutes')
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
