from django.shortcuts import render

def home(request):
  return render(request, 'home.html')# Create your views here.

def signup(request):
  return render(request, 'signup.html')
  
def myroutes(request):
  return render(request, 'myroutes.html')
