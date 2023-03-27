from django.urls import path, re_path

from . import views

app_name = "chat"
urlpatterns = [
    path("chat/", views.chatpage, name="chat-page"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("roomselect/<int:id>/", views.roomselect, name="roomselect"),
    path('chat/get_users/<term>', views.get_users, name='get_users'),
    re_path(r'^$', views.userlogin,name="login"),
    re_path(r'^logout/$', views.userlogout,name="logout"),
    re_path(r'^signup/$', views.usersignup,name="signup"),
]