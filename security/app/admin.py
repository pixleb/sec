from django.contrib import admin
from django.contrib.auth.models import User

from .models import SecObject, UserMisc

admin.site.register(SecObject)
admin.site.register(UserMisc)
