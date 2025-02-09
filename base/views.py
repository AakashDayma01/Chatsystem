from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic ,Message
from .forms import Roomform ,Topicform , MessageForm
from django.db.models import Q 
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm ,CustomUserUpdateForm
import base64
import re
from django.core.files.base import ContentFile
# Create your views here.

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username , password = password)
        except:
            messages.error(request,"User does not exist")

        user = authenticate(request, username = username , password=password)

        if user is not None:
            login(request , user)
            return redirect('Home')
        else:
            messages.error(request , "Username or Password does not exists ")

    mydata = request.session.get('mydata', None)
    if mydata:
        passusername = str(mydata['first_name'] +" "+mydata['last_name'])
    else:
        passusername = None

    context = {'page':page, 'mydata':mydata , 'username':passusername} 
    return render(request ,'base/login_register.html' , context)

def logoutuser(request):
    logout(request)
    return redirect('Home')

def registeruser(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = str(user.first_name +" "+user.last_name) 
            
            image_data = request.POST.get('image')
            if image_data:
                image_data = re.sub('^data:image\/(png|jpeg);base64,', '', image_data)
                image_data = base64.b64decode(image_data)
                user.image.save('captured_image.jpg', ContentFile(image_data) ,save = False) 
            user.save()
            request.session['mydata'] = request.POST
            return redirect('login')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    rooms = Room.objects.none()
    if request.user.is_authenticated:
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        rooms = Room.objects.filter(
            Q(participants=request.user)
        ).filter(
            Q(topic__Topic_name__icontains=q) |  
            Q(name__icontains=q) |  
            Q(description__icontains=q)  
        )
        if rooms.exists():
            room_messages = Message.objects.filter(room__in=rooms)
            topics = Topic.objects.filter(room__in=rooms).distinct()
            unique_topics = []
            for topic in topics:
                topic = topic.Topic_name.capitalize()
                if topic not in unique_topics:
                    unique_topics.append(topic)         
        else:
            room_messages = None
            unique_topics = None

    else:
        unique_topics = None
        room_messages = None
    room_count = rooms.count()


    context = {'rooms': rooms , 'unique_topics':unique_topics,'room_count':room_count , 'room_messages':room_messages}
    return render (request ,'base/home.html',context)

@login_required(login_url="/login")
def room(request , pk):
    rooms = Room.objects.get(id = pk)
    messages = rooms.message_set.all()
    participants = rooms.participants.all()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES) 
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = rooms
            message.save()
            rooms.participants.add(request.user)
            return redirect('Room', pk=rooms.id)

    form = MessageForm()
    context = {'room_name': rooms, 'messages': messages, 'participants': participants, 'form': form}

    return render(request,'base/room.html',context)


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.values('Topic_name').distinct()
    unique_topics = []
    for topic in topics:
        t = topic['Topic_name'].lower()
        topic = t.capitalize()
        if topic not in unique_topics:
            unique_topics.append(topic)
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'unique_topics':unique_topics}
    return render(request,'base/profile.html',context)

@login_required(login_url="/login")
def createroom(request):
    if request.method == 'POST':
        form = Roomform(request.POST)
        Topic_form = Topicform(request.POST)
        if form.is_valid() and Topic_form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            topic = Topic_form.save()
            room.topic = topic  
            room.save() 
            participants = form.cleaned_data.get('participants')
            if participants:
                print(participants)
                room.participants.set(participants)
            room.participants.add(request.user)
            return redirect('Home')
    Topic_form = Topicform()
    form = Roomform()
    context = {'form':form , 'Topic_form':Topic_form}
    return render(request ,"base/room_form.html", context)

@login_required(login_url="/login")
def updateroom(request,pk):
    room = Room.objects.get(id = pk)
    topic = room.topic 
    Topic_form = Topicform(instance=topic) 
    form = Roomform(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed here ")

    if request.method == 'POST':
        form = Roomform(request.POST , instance=room)
        Topic_form = Topicform(request.POST , instance=topic)
        if form.is_valid():
            Topic = Topic_form.save()
            form.save(commit = False)
            form.topic = Topic
            form.save()
            return redirect('Home')
    context = {'form':form , 'Topic_form':Topic_form}
    return render(request,'base/room_form.html',context)

@login_required(login_url="/login")
def deleteroom(request , pk):
    room = Room.objects.get(id=pk)
    topic_name= room.topic 
    print(topic_name)
    if request.user != room.host:
        return HttpResponse("You are not allowed here ")
    
    if request.method == 'POST':
        room.delete()
        topic_name.delete()
        return redirect('Home')
    return render(request, 'base/delete.html',{'obj':room})


@login_required(login_url="/login")
def deletemessage(request , pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here ")
    
    if request.method == 'POST':
        message.delete()
        return redirect('Home')
    return render(request, 'base/delete.html',{'obj':message})

def deleteprofile(request , pk):
    user = User.objects.get(id = pk)
    username = user.username
    if request.method == 'POST': 
        user.delete()
        return redirect ('Home')
    
    return render(request,'base/deleteprofile.html', {'username':username })

def UpdateProfile(request , pk):
    user = User.objects.get(id = pk)
    form = CustomUserUpdateForm(instance = user)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            image_data = request.POST.get('image')
            if image_data:
                image_data = re.sub('^data:image\/(png|jpeg);base64,', '', image_data)
                image_data = base64.b64decode(image_data)
                user.image.save('captured_image.jpg', ContentFile(image_data) ,save = False) 
            user.save()
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request, 'An error occurred during Updating profile')
    return render(request, 'base/updateuser.html', {'form': form})
