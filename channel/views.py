from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from channel.forms import SignUp, LoginForm, FileForm
from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from datetime import datetime
# Create your views here.

def is_loggedin(request):
    status = request.user.is_authenticated
    if status:
        show = request.user.username[0].upper()
    else:
        show = None  
    return status,show

def index(request):
    status,show = is_loggedin(request)  
    return render(request,'channel/home.html',{'show':show,'status':status})

@login_required
def homepage(request,groupname):
    from channel.models import ChatMessages,Groupname
    chat = None
    user_name = request.user.username[0]
    group, created = Groupname.objects.get_or_create(group=groupname)
    print(created,"hi")
    file_form = FileForm(initial={'user':request.user.username,'groupname':group,"messages":''})
    if not created:
        if group.member_count > 0:
            chat = ChatMessages.objects.filter(groupname=group.id)
        else:
            present_time = datetime.now()
            # last_active_time = datetime.strptime(group.last_active,'%Y-%m-%d %H:%M:%S')
            last_active_time = group.last_active
            print(present_time)
            print(last_active_time)
            try:
                date_format = "%Y-%m-%d %H:%M:%S"
                last_active_time = datetime.strptime(last_active_time, date_format)
            except:
                date_format = "%Y-%m-%d %H:%M:%S.%f"
                last_active_time = datetime.strptime(last_active_time, date_format)
            # Calculate the difference
            time_difference = present_time - last_active_time
            # Convert the difference to seconds
            difference_seconds = time_difference.total_seconds()
            if difference_seconds >10.0:
                group.delete()
                print("delete")
                group, created = Groupname.objects.get_or_create(group=groupname)
    if request.method == 'POST':
        file_form = FileForm(request.POST,request.FILES)
        if file_form.is_valid():
            data = file_form.save()
            file_url = data.file.url
            layer_name = get_channel_layer()
            user_data = {'user':request.user.username,'status':'image-uploaded-done',"url":file_url}
            user_data_json = json.dumps(user_data)
            async_to_sync(layer_name.group_send)(
                groupname,
                {
                    "type": "chat.message", 
                    "text":user_data_json
                })
    return render(request,'channel/index.html',{'chat':chat,'groupname':group,'user':user_name,'form':file_form})

def signup(request):
    form = SignUp()
    if request.method =='POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registered Successfully')
    return render(request,'channel/signup.html',{'form':form})

def loginpage(request):
    from channel.models import ChatMessages,Groupname
    form = LoginForm()
    if request.method =='POST':
        print(request.POST)
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            print(form.is_valid())
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            groupname = request.POST['groupname']
            user = authenticate(username=username,password=password)
            if user:
                group = Groupname.objects.filter(group=groupname)
                print(group)
                if len(group)==0:
                    login(request,user)
                    return redirect(f'/group/{groupname}/')
                else:
                    if group[0].private and group[0].member_count>0:
                        messages.error(request,'This group is private')
                    else:
                        group.update(private=False)
                        login(request,user)
                        return redirect(f'/group/{groupname}/')
    return render(request,'channel/login.html',{'form':form})

def logoutpage(request):
    logout(request)
    return redirect('/login/')

def Groupmessage(groupname,file_url,user):
    print(groupname,file_url,user)
    layer_name = get_channel_layer()
    user_data = {'user':user,'status':'image-uploaded-done',"url":file_url}
    user_data_json = json.dumps(user_data)
    async_to_sync(layer_name.group_send)(
        groupname,
        {
            "type": "chat.message", 
            "text":user_data_json
        })
    return None