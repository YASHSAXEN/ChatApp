from django.db import models
from datetime import datetime

# Create your models here.
class Groupname(models.Model):
    group = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    member_count = models.IntegerField(default=0)
    member = models.TextField(blank=True,default='')
    last_active = models.CharField(max_length=150, blank=True, null=True, default=f'{datetime.now()}')

    def __str__(self):
        return self.group

class ChatMessages(models.Model):
    groupname = models.ForeignKey(Groupname,on_delete=models.CASCADE)
    user = models.CharField(max_length=30)
    message = models.CharField(max_length=200,blank=True)
    file = models.ImageField(upload_to='images',blank=True)
    message_time = models.TimeField(auto_now=True)