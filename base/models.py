from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.

class Topic(models.Model):
    Topic_name = models.CharField(max_length = 200)
    def __str__(self):
        return self.Topic_name


class User(AbstractUser ):
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=15, blank=True , unique = True) 
    qualifications = models.TextField(blank=True)
    address = models.TextField(blank=True) 
    image = models.ImageField(upload_to='profile_images/', default='default.jpg')

    def __str__(self):
        return self.username
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null = True) 
    name = models.CharField( max_length=200)
    description = models.TextField(null = True , blank = True)
    participants = models.ManyToManyField(User , related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user =models.ForeignKey(User,on_delete = models.CASCADE) 
    room = models.ForeignKey(Room,on_delete =  models.CASCADE)
    body = models.TextField(blank=True , null=True)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)  # For image messages
    file = models.FileField(upload_to='message_files/', blank=True, null=True)  # For file messages
    video = models.FileField(upload_to='message_videos/', blank=True, null=True)  # For video messages
    audio = models.FileField(upload_to='message_audios/', blank=True, null=True)  # For audio messages
    link = models.URLField(blank=True, null=True)  # For sharing links
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['updated','created']

    def __str__(self):
        return self.body[0:50] if self.body else "No Content"
    


    



