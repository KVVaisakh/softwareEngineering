from django.urls import path
from chat import views


urlpatterns = [
	path('', views.index, name='chat'),
	path('stable', views.stable, name='chatStable'),
	path('DMHistory', views.DMHistory, name='DMHistory'),
	path('DMHistoryDatabase',views.DMHistoryDatabase,name='DMHistoryDatabase'),
	path('continueChat/<str:name>', views.continueChat, name='continueChat'),
	path('continueGroupChat/<str:team>', views.continueGroupChat, name='continueGroupChat'),
	path('chatNow', views.chatNow, name='chatNow'),
	path('groupChatNow', views.groupChatNow, name='groupChatNow'),
]
