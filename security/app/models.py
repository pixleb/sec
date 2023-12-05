from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# on top because used in almost all models as a foreign key
class SecObject(models.Model):
    name = models.CharField(max_length = 128)


# users
class UserMisc(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length = 16, default = 'user')
    obj = models.ForeignKey(SecObject, on_delete = models.CASCADE)

    
# security
class LockModel(models.Model):
    name = models.CharField(max_length = 128)
    
    # transited in json
    mac = models.CharField(max_length = 128)
    status = models.IntegerField(default = 0)
    power = models.IntegerField(default = 0)
    updated = models.DateTimeField(default = datetime.now())
    
    # lock command response
    command = models.CharField(max_length = 64, default = 'none')
    state = models.CharField(max_length = 64, default = 'Закрыт')
    inverse = models.BooleanField(default = False)
    
    obj = models.ForeignKey(SecObject, on_delete = models.CASCADE)
    
class CameraModel(models.Model):
    name = models.CharField(max_length = 128)
    rtsp = models.CharField(max_length = 128)
    
    obj = models.ForeignKey(SecObject, on_delete = models.CASCADE)
    