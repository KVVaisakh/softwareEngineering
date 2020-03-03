from django.urls import path
from team import views

urlpatterns = [
    path('', views.index, name='team'),
    path('new', views.newTeam, name='newTeam'),
    path('<str:name>/editTimeline', views.editTimeline, name='editTimeline'),
    path('<str:name>/addMembers',views.addMembers, name='addMembers'),
    path('<str:name>/edit/', views.editTeam, name='editTeam'),
    path('<str:name>/viewTimeline', views.viewTimeline, name='viewTimeline'),
    path('<str:name>/viewMembers',views.viewMembers, name='viewMembers'),
    path('<str:name>/view/', views.viewTeam, name='viewTeam'),
]