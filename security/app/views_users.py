'''

    Here lies main user funcs: user login/logout, superuser, admin and default user creation.

'''


# django imports
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

# django models
from .models import UserMisc, SecObject
from .forms import UserForm

# modules
from .mail.notify_admin import NotifyAdmin
from .mail.notify_user import NotifyUser


# auth
@require_http_methods(['GET', 'POST'])
def auth(request):
    try:
        if request.user.is_authenticated:
            print('user already authenticated.')
            return HttpResponseRedirect('/')
    
        if request.method == 'POST':
            if request.user.is_authenticated:
                print('user already authenticated in post')
                return HttpResponse(f'''Вы уже авторизованы как {request.user.username}. Пожалуйста, вернитесь и выйдите из профиля, прежде чем авторизоваться в другом профиле.''')
        
            print('started form validation')
            form = UserForm(request.POST)
        
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
        
                user = authenticate(request, username=username, password=password)
            
                if user is not None:
                    login(request, user)
                    print('logged in as', user.username)
                
                    userdata = UserMisc.objects.filter(owner = user)
                    print('userdata', userdata, len(userdata))
                    if not len(userdata):
                        newdata = UserMisc(owner = user)
                        newdata.save()
                        print('new usermisc created')
                
                    return HttpResponseRedirect('/')
            
                else: return render(request, 'users/auth_invalid.html', { 'form': form })
            else: return render(request, 'users/auth_invalid.html', { 'form': UserForm() })
        else: return render(request, 'users/auth.html', { 'form': UserForm() })
    
    except:
        if request.user.is_authenticated:
            print('user already authenticated in post')
            return HttpResponse(f'''
                Вы уже авторизованы как {request.user.username}. 
                Пожалуйста, вернитесь и выйдите из профиля, прежде чем авторизоваться в другом профиле.
            ''')
        else: 
            print('unknown error')
            return HttpResponse('Неизвестная ошибка.')


@require_http_methods(['GET'])
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/auth/')


@require_http_methods(['GET', 'POST'])
def create_user(request, obj):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'admin': return HttpResponseRedirect('/auth/')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            secobj = SecObject.objects.get(pk = obj)
            if secobj is None: return HttpResponse('Ошибка. Данный объект не найден.')
            
            user = User.objects.create_user(username = username, email = username, password = password)
            user.save()
            
            if user is not None:
                newdata = UserMisc(owner = user, role = 'user', obj = secobj)
                newdata.save()
                print('new usermisc created')
                
                user_notification: NotifyUser = NotifyUser(username, password)
                
                return HttpResponseRedirect('/')
            
            else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')
        else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')  
    else: return render(request, 'users/create_user.html', { 'form': UserForm() })

@require_http_methods(['GET', 'POST'])
def create_admin(request, obj):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'super': return HttpResponseRedirect('/auth/')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            secobj = SecObject.objects.get(pk = obj)
            if secobj is None: return HttpResponse('Ошибка. Данный объект не найден.')
            
            user = User.objects.create_user(username = username, email = username, password = password)
            user.save()
            
            if user is not None:
                newdata = UserMisc(owner = user, role = 'admin', obj = secobj)
                newdata.save()
                print('new usermisc created')
                
                admin_notification: NotifyAdmin = NotifyAdmin(username, password)
                
                return HttpResponseRedirect(f'/obj/{obj}/')
            
            else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')
        else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')
    else: return render(request, 'users/create_admin.html', { 'form': UserForm() })

