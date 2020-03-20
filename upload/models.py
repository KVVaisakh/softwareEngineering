from django.db import models
from django.contrib.auth.models import User
from team.models import Team,Timeline

class File(models.Model):
    name = models.CharField(max_length=255, blank=True)
    teamName = models.ForeignKey(Team,on_delete=models.CASCADE)
    task = models.ForeignKey(Timeline,on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	title=str(self.teamName)+" - "+str(self.task)
    	return title