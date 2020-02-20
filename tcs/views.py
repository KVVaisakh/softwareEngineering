from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm

def index(request):
    return render(request, 'home.html', {})

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data
			username = user['username']
			email =  user['email']
			password =  user['password']
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				User.objects.create_user(username, email, password)
				user = authenticate(username = username, password = password)
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return render(request, 'register.html', {'form' : form, 'error':"username/emailid already exists"})
	else:
		form = UserRegistrationForm()
	return render(request, 'register.html', {'form' : form})