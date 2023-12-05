'''

    Here we have backend of main security instances: objects, cameras, etc

'''


# django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

# django modules
from .models import UserMisc, SecObject, LockModel, CameraModel
from .forms import ObjectForm, LockForm, CameraForm

# miscellaneous imports
import json
from datetime import datetime
import cv2
import threading


# main code
# all the funcs decorated with @require_http_methods() are views.
# note that objects, locks and all the objects are actually being shown in views.py in def index

# electronic locks
@require_http_methods(['GET', 'POST'])
def create_lock(request, obj):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'admin': return HttpResponseRedirect('/auth/')  
    
    if request.method == 'POST':
        form = LockForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            mac = form.cleaned_data['mac']
            
            obj = SecObject.objects.get(pk = obj)
            
            lock = LockModel(name = name, mac = mac, obj = obj, updated = datetime.now())
            lock.save()
            
            return HttpResponseRedirect('/')

        else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')
    else: return render(request, 'security/create_lock.html', { 'form': LockForm() })

# i know i should have putted delete method here, but i don't care
@require_http_methods(['GET'])
def delete_lock(request, lock_id):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'admin': return HttpResponseRedirect('/auth/')  
    
    lock = LockModel.objects.get(pk=lock_id)
    lock.delete()
    
    return HttpResponseRedirect('/')
    
# api views, responses with an json
# i should've made it django-rest api view with a serializer, but i don't care
@require_http_methods(['GET'])
def get_locks(request, obj):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role not in ['admin', 'user']: 
        return HttpResponse('You have no access to fetched resource.', status = 403)
    
    locks = LockModel.objects.filter(obj = obj)
    res = serializers.serialize('json', locks)
    return HttpResponse(res)

@csrf_exempt
@require_http_methods(['POST'])
def post_lock(request):
    body = json.loads(request.body.decode('utf-8'))
    mac = body['mac']
    status = body['status']
    power = body['power']

    lock = get_object_or_404(LockModel, mac = mac)
    
    lock.mac, lock.status, lock.power = mac, status, power
    lock.updated = datetime.now()
    lock.save()
    res = {
        'command': lock.command,
        'inverse': lock.inverse,
    }
    
    return HttpResponse(json.dumps(res), status = 200)
    
@csrf_exempt
@require_http_methods(['POST'])
def post_command(request):
    # contains lock id and command
    print('posted command')
    body = json.loads(request.body.decode('utf-8'))
    mac = body['mac']
    command = body['command']
    print(mac, command)

    lock = get_object_or_404(LockModel, mac = mac)
    print(lock)
    
    if   command not in ('open', 'close', 'calibrate'): return HttpResponse('incorrect command', status = 404)
    if   command == 'open': lock.state = 'Открыт'
    elif command == 'close': lock.state = 'Закрыт'
    lock.command = command
    lock.save()
    
    return HttpResponse('ok', status = 200)
    
@csrf_exempt
@require_http_methods(['POST'])
def post_inverse(request):
    # contains lock id and command
    body = json.loads(request.body.decode('utf-8'))
    mac = body['mac']

    lock = get_object_or_404(LockModel, mac = mac)
    
    lock.inverse = not lock.inverse
    lock.save()
    
    return HttpResponse('ok', status = 200)
    
    
    
# cameras
camera_debug = False

class VideoCamera(object):
    def __init__(self, rtsp):
        self.video = cv2.VideoCapture(rtsp)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# debug
cameras_on = True

testcam = 0
#if camera_debug: testcam = VideoCamera("rtsp://zephyr.rtsp.stream/pattern?streamKey=b8da699715b036d24e4b39ebfa7fdc1d")
        
# creates camera stream, if it not exists
cameras = dict()

def upd_cam(cam_id):
    global cameras
    if not (cam_id in cameras):
        cam_model = CameraModel.objects.get(pk=cam_id)
        #print('creating new camera with id/name/rtsp: ', cam_model.id, cam_model.name, cam_model.rtsp)
        cameras[cam_id] = VideoCamera(cam_model.rtsp)
        #cameras[cam_id] = VideoCamera("rtsp://zephyr.rtsp.stream/pattern?streamKey=b8da699715b036d24e4b39ebfa7fdc1d")
        #print(cameras)

        
# views

@require_http_methods(['GET'])
def get_camera(request, cam_id):
    if not cameras_on: return HttpResponse('cameras are off')
    
    global cameras
    cam = cameras[cam_id]
    #print('camera is: ', cam)
    resp = StreamingHttpResponse(gen(cam))
    resp['Content-Type'] = "multipart/x-mixed-replace;boundary=frame"
    return resp


@require_http_methods(['GET', 'POST'])
def create_camera(request, obj):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'admin': return HttpResponseRedirect('/auth/')  
    
    if request.method == 'POST':
        form = CameraForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            rtsp = form.cleaned_data['rtsp']
            
            camera = CameraModel(name = name, rtsp = rtsp, obj = SecObject.objects.get(pk=obj))
            camera.save()
            
            return HttpResponseRedirect('/')

        else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')
    else: return render(request, 'security/create_camera.html', { 'form': CameraForm() })

# i know i should have putted delete method here, but i don't care
@require_http_methods(['GET'])
def delete_camera(request, cam_id):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'admin': return HttpResponseRedirect('/auth/')  
    
    cam = CameraModel.objects.get(pk=cam_id)
    cam.delete()
    
    return HttpResponseRedirect('/')

@require_http_methods(['GET'])
def test_camera(request):
    if not cameras_on: return HttpResponse('cameras are off')
    return render(request, 'security/test_camera.html')

@require_http_methods(['GET'])
def test_camera_api(request):
    if not cameras_on: return HttpResponse('cameras are off')
    
    global testcam
    #print('camera is: ', testcam)
    resp = StreamingHttpResponse(gen(testcam))
    resp['Content-Type'] = "multipart/x-mixed-replace;boundary=frame"
    return resp

 
    
# objects code
# in an open_obj view we have main security code:
# all the locks, cameras etc must be shown here
@require_http_methods(['GET'])
def open_obj(request, obj):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'super': return HttpResponseRedirect('/auth/')
    
    obj = SecObject.objects.get(pk = obj)
    
    admins: list = list()
    miscquery = UserMisc.objects.filter(obj = obj, role = 'admin')
    for each_misc in miscquery: admins.append(each_misc.owner)
        
    return render(request, 'security/obj.html', { 'obj': obj, 'admins': admins })

@require_http_methods(['GET', 'POST'])
def create_object(request):
    user = request.user
    role = UserMisc.objects.filter(owner = user).first().role
    
    if not user.is_authenticated or role != 'super': return HttpResponseRedirect('/auth/')  
    
    if request.method == 'POST':
        form = ObjectForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            
            secobj = SecObject(name = name)
            secobj.save()
            
            return HttpResponseRedirect('/')

        else: return HttpResponse('Ошибка. Проверьте введенные данные и обратитесь к разработчику.')
    else: return render(request, 'security/create_object.html', { 'form': ObjectForm() })

    