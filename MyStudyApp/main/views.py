from pydoc_data.topics import topics

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.context_processors import request
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    context = {'page': page}
    return render(request, 'main/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registeruser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, 'An error occurred during registration')
    return render(request, 'main/register.html', {'form': form, })


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    roomcount = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'roomcount': roomcount, 'room_messages': room_messages,}
    return render(request, 'main/home.html', context)


def room(request, key):
    room = Room.objects.get(id=key)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', key=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants,}
    return render(request, 'main/room.html', context)

def userProfile(request, key):
    user = User.objects.get(id=key)
    room_messages = user.message_set.all()
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics,}
    return render(request, 'main/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            Host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form,'topics': topics}
    return render(request, 'main/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, key):
    room = Room.objects.get(id=key)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.Host:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic = topic
        room.description= request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form,'room': room, 'topics': topics}
    return render(request, 'main/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, key):
    room = Room.objects.get(id=key)
    if request.user != room.Host:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, key):
    message = Message.objects.get(id=key)

    if request.user != message.user:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile', key=user.id)
    return render(request, 'main/update-user.html', {'form': form})


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'main/topic.html', {'topics': topics})

def activiyPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Room.objects.all()
    return render(request, 'main/active.html', {'room_messages': room_messages})