import os, sys
sys.path.insert(0, '/home/i/i952607q/lombard/public_html/')
sys.path.insert(1, '/home/i/i952607q/.local/lib/python3.6/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dj4.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()