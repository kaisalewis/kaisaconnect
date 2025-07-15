from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registeruser, name='register'),
    path('', views.home, name='home'),
    path('room/<str:key>/', views.room, name='room'),
    path('userprofile/<str:key>/', views.userProfile, name='userprofile'),
    path('createroom/', views.createRoom, name='createroom'),
    path('updateroom/<str:key>/', views.updateRoom, name='updateroom'),
    path('deleteroom/<str:key>/', views.deleteRoom, name='deleteroom'),
    path('deletemessage/<str:key>/', views.deleteMessage, name='deletemessage'),
    path('update-user', views.updateUser, name='update-user'),
    path('topics', views.topicPage, name='topics'),
    path('recent', views.activiyPage, name='recent'),
]
