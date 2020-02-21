from django.shortcuts import render
from . import models
from django.shortcuts import redirect
from django.utils import timezone
from .models import DirectMessage,GroupMessage
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UsernameForm,DirectMessageForm
from django import forms
from team.models import TeamMember

def index(request):
	chats=models.DirectMessage.objects.filter(Q(sentFrom=request.user) |  Q(sentTo=request.user)).order_by('created_date').reverse()
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
	groupChat=[]
	for team in teams:
		groupChat.append(models.GroupMessage.objects.filter(Q(sentTo=team)))
	return render(request, 'chatHistory.html', {'chats':chatList, 'groupChats':groupChat, 'user':request.user})

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
		nameId=models.User.objects.get(username=name)
		print(name,nameId)
		chats=models.DirectMessage.objects.filter((Q(sentFrom=request.user) &  Q(sentTo=nameId)) | (Q(sentFrom=nameId) &  Q(sentTo=request.user))).order_by('created_date')
		form=DirectMessageForm(initial={'sentTo':nameId})
		form.fields['sentTo'].widget = forms.HiddenInput()
	return render(request, 'message.html', {'form': form,'chats':chats,'name':name})

# def continueGroupChat(request,name):
# 	if request.method == "POST":
# 		form = GroupMessageForm(request.POST)
# 		if form.is_valid():
# 			chat=form.save(commit=False)
# 			chat.created_date=timezone.now()
# 			chat.sentFrom=request.user
# 			chat.save()			
# 			return redirect('continueChat',name=name)	
# 	else:
# 		nameId=models.User.objects.get(username=name)
# 		print(name,nameId)
# 		chats=models.DirectMessage.objects.filter((Q(sentFrom=request.user) &  Q(sentTo=nameId)) | (Q(sentFrom=nameId) &  Q(sentTo=request.user))).order_by('created_date')
# 		form=GroupMessageForm(initial={'sentTo':nameId})
# 		form.fields['sentTo'].widget = forms.HiddenInput()
# 	return render(request, 'message.html', {'form': form,'chats':chats,'name':name})
