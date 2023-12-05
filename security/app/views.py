'''

    This is main views class, that imports all the other views.

'''

# django imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

# django modules
from .models import UserMisc, SecObject, LockModel

# views
from .views_users import *
from .views_security import *


# main
def index(request):
    if not request.user.is_authenticated: return HttpResponseRedirect('/auth/')
    
    user = request.user
    
    userdata = UserMisc.objects.filter(owner = user)
    if not len(userdata): return HttpResponseRedirect('/auth/')
    data = userdata.first()
    
    if data.role == 'super': 
        objects = SecObject.objects.all()
        return render(request, 'index.html', { 'role': data.role, 'objects': objects })
    
    elif data.role == 'admin': 
        obj = data.obj
        users: list = list()
        
        userquery = UserMisc.objects.filter(obj = obj, role = 'user')
        for each_user in userquery: users.append(each_user.owner)
        
        locks = LockModel.objects.filter(obj = obj)
        
        cameras = CameraModel.objects.filter(obj = obj)
        for each_camera in cameras: upd_cam(each_camera.id)
        
        return render(request, 'index.html', { 
            'role': data.role, 'obj': data.obj, 'users': users, 'locks': locks, 'cameras': cameras,
        })
    
    elif data.role == 'user': 
        return render(request, 'index.html', { 'role': data.role, 'obj': data.obj })
    
    else: return HttpResponse('role is incorrect.')
    

 
