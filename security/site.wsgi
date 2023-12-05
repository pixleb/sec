import os, sys, logging

test = 1

domain = 'a0845167.xsph.ru'
login = 'a0845167'
project = 'greenery'

if(test):
    logging.info('{domain}, {login}, {project}')
    exit()

activate_this = '/home/{login}/python/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})
sys.path.insert(0, os.path.join('/home/{login}/domains/{domain}/myproject'))
os.environ['DJANGO_SETTINGS_MODULE'] = '{project}.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()