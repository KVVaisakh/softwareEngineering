from django.urls import path
from team import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.enterTeamDetails, name='enterTeamDetails'),
    path('<str:name>/addMembers',views.addMembers, name='addMembers'),
    path('<str:name>/edit/', views.teamEdit, name='teamEdit'),
    path('<str:name>/display/', views.teamDisplay, name='teamDisplay'),
]