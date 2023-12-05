from django import forms

# users
class UserForm(forms.Form):
    username = forms.CharField(label = 'Логин', max_length = 64)
    password = forms.CharField(label = 'Пароль', max_length = 64)
    
# security
class ObjectForm(forms.Form):
    name = forms.CharField(label = 'Название объекта', max_length = 128)

class LockForm(forms.Form):
    name = forms.CharField(label = 'Название замка', max_length = 128)
    mac = forms.CharField(label = 'MAC адрес:', max_length = 128)

class CameraForm(forms.Form):
    name = forms.CharField(label = 'Название камеры', max_length = 128)
    rtsp = forms.CharField(label = 'RTSP адрес:', max_length = 128)
    