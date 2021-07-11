from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse, request
from django.contrib.auth.models import User, auth

# Create your views here.
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username,password=password)
    
    if user is not None:
      auth.login(request,user)
      return redirect('/create/')

    else:
      messages.warning(request,'Invalid Credentials')
      return redirect('/accounts/login')

  else:
    return render(request,'enroll/login.html')

def logout(request):
  auth.logout(request)
  return redirect('/accounts/login')