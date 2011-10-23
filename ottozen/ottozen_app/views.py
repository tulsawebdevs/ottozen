from django.shortcuts import render
from django.views.generic.create_update import create_object

from models import Route

def home(request):
  return render(request, 'home.html')# Create your views here.

def old_add(request):
  return create_object(request, model=Route, login_required=True,
    post_save_redirect='/commutes/add')
