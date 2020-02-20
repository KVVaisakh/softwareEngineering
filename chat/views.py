from django.shortcuts import render
from . import models
from .models import DirectMessage,GroupMessage
from django.db.models import Q

def index(request):
	chats=models.DirectMessage.objects.filter(Q(sentFrom=request.user) |  Q(sentTo=request.user))
	return render(request, 'chatHistory.html', {'chats':chats, 'user':request.user})

def chatNow(request,name):
	if request.method == "POST":
		form = DirectMessageForm(request.POST)
		if form.is_valid():
			chat=form.save(commit=False)
			chat.created_date=timezone.now()
			chat.sentFrom=request.user
			chat.sentTo=name
			chat.save()			
			return redirect('index')
	else:
		form=DirectMessageForm()
	return render(request, 'message.html', {'form': form})