from django.urls import path
from chat import views

urlpatterns = [
	path('', views.index, name='index'),
	path('<str:name>/chatNow', views.chatNow, name='chatNow')
]