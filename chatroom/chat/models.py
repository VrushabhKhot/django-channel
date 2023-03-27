from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=16, blank=True, null=True)

	def __str__(self):
		return self.user.username

class ChatRoom(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Chat(models.Model):
	content = models.CharField(max_length=1000)
	timestamp = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	
	def __str__(self):
		return self.content