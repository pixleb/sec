from django.contrib import admin
from django.urls import path

from django.views.generic import TemplateView

import app.views as app

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', app.index),
    
    # users
    path('auth/', app.auth),
    path('logout/', app.logout_user),
    
    path('create_admin/<int:obj>/', app.create_admin),
    path('create_user/<int:obj>/', app.create_user),
    
    # security
    path('obj/<int:obj>/', app.open_obj),
    path('create_object/', app.create_object),
    
    # promise routes
    path('create_lock/<int:obj>/', app.create_lock),
    path('get_locks/<int:obj>/', app.get_locks),
    path('post_lock/', app.post_lock),
    path('post_command/', app.post_command),
    path('post_inverse/', app.post_inverse),
    
    #cameras
    path('test_camera/', app.test_camera),
    path('test_camera_api/', app.test_camera_api, name = 'test_camera_api'),
    path('create_camera/<int:obj>/', app.create_camera),
    path('get_camera/<int:cam_id>/', app.get_camera),
    path('delete_camera/<int:cam_id>/', app.delete_camera),
]
