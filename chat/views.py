from django.shortcuts import render
from . import models
from django.shortcuts import redirect
from django.utils import timezone
from .models import DirectMessage,GroupMessage
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import *
from django import forms
from team.models import *
from django.contrib.auth.decorators import login_required
from tcs.decorators import *
import json
from django.http import JsonResponse
from django.core import serializers

def stable(request):
	chats=DirectMessage.objects.filter(Q(sentFrom=request.user) |  Q(sentTo=request.user)).order_by('created_date').reverse()
	chatList=[]
	chattedWith=set()
	companion=""
	for chat in chats:
		if chat.sentTo==request.user:
			companion=chat.sentFrom
		else:
			companion=chat.sentTo
		if companion not in chattedWith:
			chattedWith.add(companion)
			chatList.append(chat)

	teamObj=TeamMember.objects.filter(Q(userName=request.user))
	teams=[]
	for team in teamObj:
		teams.append(team.teamName)
	groupChats=[]
	for team in teams:
		groupChats.append(GroupMessage.objects.filter(Q(sentTo=team)).order_by('-created_date')[:1])
	return render(request, 'chatHistory.html', {'chats':chatList, 'groupChats':groupChats, 'user':request.user,})

@login_required
def index(request):
	chats=DirectMessage.objects.filter(Q(sentFrom=request.user) |  Q(sentTo=request.user)).order_by('created_date').reverse()
	chatList=[]
	chattedWith=set()
	companion=""
	for chat in chats:
		if chat.sentTo==request.user:
			companion=chat.sentFrom
		else:
			companion=chat.sentTo
		if companion not in chattedWith:
			chattedWith.add(companion)
			chatList.append(chat)

	return render(request, 'mainChat.html', {'chats':chatList, 'user':request.user})

@login_required
def chatNow(request):
	if request.method == "POST":
		form = DirectMessageForm(request.POST)
		if form.is_valid():
			chat=form.save(commit=False)
			chat.created_date=timezone.now()
			chat.sentFrom=request.user
			chat.save()
			return redirect('continueChat',name=chat.sentTo)
	else:
		form=DirectMessageForm()
	return render(request, 'message.html', {'form': form})

@login_required
def groupChatNow(request):
	if request.method == "POST":
		form = GroupMessageForm(request.POST)
		if form.is_valid():
			chat=form.save(commit=False)
			chat.created_date=timezone.now()
			chat.sentFrom=request.user
			chat.save()
			return redirect('continueGroupChat',team=chat.sentTo)
	else:
		form=GroupMessageForm()
	return render(request, 'message.html', {'form': form})

def DMHistoryDatabase(request):
	if request.method == "POST":
		form = DirectMessageFormM(request.POST)
		if form.is_valid():
			message=form.cleaned_data['message']
			sentTo=form.cleaned_data['sentTo']
			print(sentTo,message)
			sentTo=User.objects.get(username=sentTo)
			form2=DirectMessageForm({'sentTo':sentTo,'message':message})
			if form2.is_valid():
				chat=form2.save(commit=False)
				chat.created_date=timezone.now()
				chat.sentFrom=request.user
				chat.save()
				DMs=DirectMessage.objects.filter((Q(sentFrom=request.user) &  Q(sentTo=sentTo)) | (Q(sentFrom=sentTo) &  Q(sentTo=request.user))).order_by('created_date')
				return redirect('chat')
		nameId=request.POST.get('name')
		print(str(nameId)+'req')
		nameId=User.objects.get(username=nameId)
		DMs=DirectMessage.objects.filter((Q(sentFrom=request.user) &  Q(sentTo=nameId)) | (Q(sentFrom=nameId) &  Q(sentTo=request.user))).order_by('created_date')
		DMs = serializers.serialize("json", DMs)
		return JsonResponse(DMs, safe=False)
	else:
		return HttpResponse("Not post")

def DMHistory(request):
	if request.method=="POST":
		data=request.POST.get('data')
		print(data)

		deserial = serializers.deserialize("json", data)
		DMs=[]
		partner=""
		for i in deserial:
			DMs.append(i.object)
		if DMs[0].sentTo==request.user:
			partner=DMs[0].sentFrom
		else:
			partner=DMs[0].sentTo
		form=DirectMessageFormM(initial={'sentTo':partner})
		# form.fields['sentTo'].widget = forms.HiddenInput()
		return render(request,'DMHistory.html',{'DMs':DMs,'partner':partner,'form': form,})

@login_required
def continueChat(request,name):
	if request.method == "POST":
		form = DirectMessageForm(request.POST)
		if form.is_valid():
			chat=form.save(commit=False)
			chat.created_date=timezone.now()
			chat.sentFrom=request.user
			chat.save()
			return redirect('continueChat',name=name)
	else:
		nameId=User.objects.get(username=name)
		chats=DirectMessage.objects.filter((Q(sentFrom=request.user) &  Q(sentTo=nameId)) | (Q(sentFrom=nameId) &  Q(sentTo=request.user))).order_by('created_date')
		form=DirectMessageForm(initial={'sentTo':nameId})
		form.fields['sentTo'].widget = forms.HiddenInput()
	return render(request, 'message.html', {'form': form,'chats':chats,'name':name})

@login_required
@userIsMember
def continueGroupChat(request,team):
	if request.method == "POST":
		form = GroupMessageForm(request.POST)
		if form.is_valid():
			chat=form.save(commit=False)
			chat.created_date=timezone.now()
			chat.sentFrom=request.user
			chat.save()
			return redirect('continueGroupChat',team=team)
	else:
		chats=GroupMessage.objects.filter(Q(sentTo=team)).order_by('created_date')
		form=GroupMessageForm(initial={'sentTo':team})
		form.fields['sentTo'].widget = forms.HiddenInput()
	return render(request, 'message.html', {'form': form,'chats':chats,'team':team})
