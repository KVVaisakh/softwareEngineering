from django.urls import path
from chat import views

urlpatterns = [
	path('', views.index, name='index'),
	path('continueChat/<str:name>', views.continueChat, name='continueChat'),
	path('chatNow', views.chatNow, name='chatNow')
]