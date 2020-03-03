from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Team(models.Model):
    teamName = models.CharField(primary_key=True,max_length=200)
    teamLeader = models.ForeignKey(User,on_delete=models.CASCADE)
    directoryLink = models.CharField(unique=True,max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.teamName

class TeamMember(models.Model):
    teamName = models.ForeignKey(Team,on_delete=models.CASCADE)
    userName = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=200)

    class Meta:
        unique_together = (('teamName', 'userName'),)

    def __str__(self):
    	title=str(self.userName)+" - "+str(self.teamName)
    	return title

class Timeline(models.Model):
    teamName = models.ForeignKey(Team,on_delete=models.CASCADE)
    deadline = models.DateTimeField(default=timezone.now)
    task = models.CharField(unique=True,max_length=50)
    taskDetails = models.CharField(unique=True,max_length=200)

    class Meta:
        unique_together = (('teamName', 'task'),)

    def __str__(self):
        title=str(self.task)+" - "+str(self.teamName)
        return title