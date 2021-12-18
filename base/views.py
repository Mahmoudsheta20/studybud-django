from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from .models import Message, Room, Topic
from .forms import RoomForm, Userform
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# rooms = [{'id': 1, 'name': 'mahmoud'},
#          {'id': 2, 'name': 'lorem'},
#          {'id': 3, 'name': 'ansdkk'},


#          ]

def loginpage(requset):

    page = 'login'

    if requset.user.is_authenticated:
        return redirect('home')

    if requset.method == 'POST':
        username = requset.POST.get('username').lower()
        password = requset.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(requset, 'user does not exist')
        user = authenticate(requset, username=username, password=password)
        if user is not None:
            login(requset, user)
            return redirect('home')
        else:
            messages.error(requset, 'usernaem or password does not exist')

    context = {'page': page}
    return render(requset, 'base/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


def registerpage(requset):

    form = UserCreationForm()
    if requset.method == 'POST':
        form = UserCreationForm(requset.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(requset, user)
            return redirect('home')
        else:
            messages.error(requset, 'an error')
    return render(requset, 'base/login.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(descriptor__icontains=q))

    topics = Topic.objects.all()[0:5]
    topic_count = Topic.objects.all().count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    count = rooms.count()
    count_pyton = Room.objects.filter(Q(topic__name='python')).count
    context = {'rooms': rooms, 'topics': topics,
               'count': count, 'count_pyton': count_pyton, 'room_messages': room_messages, 'topic_count': topic_count}
    return render(request, 'base/home.html', context)


def room(request, pk):

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    Participants = room.participants.all()

    if request.method == 'POST':
        messages = Message.objects.create(

            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': Participants, }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):

    # form = RoomForm()

    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            descriptor=request.POST.get('descriptor'),


        )
        return redirect('home')

        # form = RoomForm(request.POST)

        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(requset, pk):

    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    if requset.user != room.host:
        return HttpResponse('your are not allwed')
    if requset.method == "POST":
        topic_name = requset.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = requset.POST.get('name')
        room.topic = topic
        room.descriptor = requset.POST.get('descriptor')
        room.save()

        return redirect('home')
    context = {'form': form, 'topics': topics,
               'room': room}
    return render(requset, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(requset, pk):
    room = Room.objects.get(id=pk)

    if requset.method == "POST":
        room.delete()
        return redirect('home')
    return render(requset, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deletemessage(requset, pk):
    message = Message.objects.get(id=pk)

    if requset.method == "POST":
        message.delete()
        return redirect('home')
    return render(requset, 'base/delete.html', {'obj': message})


def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    count = rooms.count()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics, 'count': count}
    return render(request, 'base/profil.html', context)


@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = Userform(instance=user)
    if request.method == 'POST':
        form = Userform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'base/update_user.html', {'form': form})


def topicpage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topic.html', {'topics': topics})


def activpage(request):
    # message = Message.objects.all()

    room_messages = Message.objects.all()
    return render(request, 'base/activ.html', {'room_messages': room_messages})
