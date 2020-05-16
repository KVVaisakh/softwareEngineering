from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from .forms import *
from django.core.mail import EmailMultiAlternatives
from tcs.email import *
from django.shortcuts import redirect
from django.core import signing
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import *
from team.models import UserDetail
from team.forms import UserDetailForm
import random
from .settings import MEDIA_ROOT, MEDIA_URL

def index(request):
	if request.method == 'POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data
			username = user['username']
			password =  user['password']
			user = authenticate(username = username, password = password)
			if user:
				login(request, user)
				return redirect('home',username=username)
			else:
				return render(request, 'errorconnected.html')
		else:
			return render(request, 'errorconnected.html')
	else:
		if request.user.is_authenticated:
			return redirect('home',username=request.user.username)
		form=LoginForm()
	return render(request, 'index.html', {'form':form})

@login_required
def home(request,username):
	details=UserDetail.objects.get(user=request.user)
	print(MEDIA_URL)
	return render(request, 'home1.html', {'details':details,'media_url': MEDIA_URL})

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		print("hi1")
		if form.is_valid():
			print("hi2")
			user = form.cleaned_data
			username = user['username']
			email =  user['email']
			password =  user['password']
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				otp=random.randint(100000,999999)
				sendWelcome([email],otp)
				otp=signing.dumps(otp, key='sekrit')
				password=signing.dumps(password, key='sekrit')
				request.session['username']=username
				return redirect('otp',otp=otp,username=username, email=email, password=password)
			else:
				return render(request, 'register1.html', {'form' : form, 'error':"username/emailid already exists"})
	else:
		form = UserRegistrationForm()
	return render(request, 'register.html', {'form' : form})

def otpVerification(request,otp,username, email, password):
	if request.session.has_key('username'):
		if request.method == 'POST':
			otp=signing.loads(otp, key='sekrit')
			password=signing.loads(password, key='sekrit')
			form = OtpForm(request.POST)
			if form.is_valid():
				typedOtp=form.cleaned_data['otp']
				if int(typedOtp)==int(otp):
					User.objects.create_user(username, email, password)
					user = authenticate(username = username, password = password)
					login(request, user)
					return redirect('details')
				else:
					del request.session['username']
					return render(request, 'otperror.html')
		else:
			form = OtpForm()
		return render(request, 'otp.html', {'form' : form})
	else:
		return render(request, 'errorconnected.html')

def details(request):
	if request.method == 'POST':
		form = UserDetailForm(request.POST,request.FILES)
		if form.is_valid():
			details=form.save(commit=False)
			details.photo.name = request.user.username+"/"+details.photo.name
			details.user=request.user
			details.save()
		else:
			return render(request, 'errorconnected.html')
		return HttpResponseRedirect('/')
	else:
		form = UserDetailForm()
	return render(request, 'details.html', {'form' : form})
