from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib import messages
import json

from django.contrib.sessions.models import Session
from django.utils import timezone

def get_all_logged_in_users():
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	uid_list = []

	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.get('_auth_user_id', None))

	return User.objects.filter(id__in=uid_list)


# Create your views here.
def userlogin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request,user)
				return redirect('chat:chat-page')
			else:
				return HttpResponse('Account Not active')
		else:
			print('Some ome tried to login and faild')
			print('Username: {} password {}'.format(username,password))
			messages.error(request,f"User crediantials are wrong. Please login with proper user crediantials.")
			return HttpResponseRedirect(reverse('chat:login'))
            
	else:
		if request.user.is_authenticated:
			return redirect('chat:chat-page')
		return render(request, 'chat/login.html',{})

def userlogout(request):
	logout(request)
	return HttpResponseRedirect(reverse('chat:login'))


def usersignup(request):

	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			uname = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			user_present	=	User.objects.filter(username=uname.lower()).exists()
			email_present	=	User.objects.filter(email=email.lower()).exists()
			if user_present:
				messages.error(request,f"Entered username is already exist.Please login with the existing crediantial or use different username. ")
				return render(request, 'chat/signup.html',)
			elif email_present:
				messages.error(request,f"Entered email id is already exist.Please uses different EMail id. ")
				return render(request, 'chat/signup.html',)
			else:
				user = form.save()
				user.refresh_from_db()
				phone_number =  form.cleaned_data.get('phone')
				UserProfile.objects.update_or_create(user=user, defaults={'phone_number': phone_number},)
				user.save()
				messages.info(request,f"You have successfully registered,""You can login the portal using your login credentials")
				return redirect('chat:login')
		else:
			messages.error(request,form.errors)
			return redirect('chat:signup')
	else:
		form = NewUserForm()
		return render(request, 'chat/signup.html',{'form':form})

@login_required(login_url="chat:login")
def chatpage(request):
	if not request.user.is_authenticated:
		return redirect("chat:login")
	chatroom = ChatRoom.objects.all()
	chat = Chat.objects.filter(user=request.user).update(active=False)

	users = User.objects.exclude(username=request.user.username)
	return render(request, "chat/index.html",{'chatroom':chatroom, 'user':users})



@login_required(login_url="chat:login")
def room(request, room_name):
	room = ChatRoom.objects.filter(name=room_name).first()
	chats = []
	div = room_name.split('-')
	if int(div[0]) == request.user.id:
		user_obj = User.objects.get(id=int(div[1]))
	else:
		user_obj = User.objects.get(id=int(div[0]))

	if room:
		chats = Chat.objects.filter(room=room)
	else:
		room = ChatRoom(name=room_name)
		room.save()
	
	# user = get_all_logged_in_users()
	user = User.objects.exclude(username=request.user.username)

	return render(request, 'chat/room.html', {'user': user_obj, 'room_name': room_name, 'chats': chats,'active_users':user})

@login_required(login_url="chat:login")
def roomselect(request, id):
	i = request.user.id
	j = id
	add=""
	if i < j:
		add = str(i)+'-'+str(j)
	elif i>j :
		add = str(j)+'-'+str(i)
	
	chats = ChatRoom.objects.filter(name=add)
	if not chats:
		room = ChatRoom(name=add)
		room.save()
	return redirect('chat:room', room_name=add)

# This is for Autocomplete search for users
@login_required(login_url="chat:login")
def get_users(request,term):
	if request.method == 'GET':
		users = User.objects.filter(username__icontains = term )[:20]
		print(users)
		results = []
		for i in users:
			user_json = {}
			user_json['id'] = i.id
			user_json['label'] = i.username
			user_json['value'] = i.username
			results.append(user_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)	






