import os
from vercel_wsgi import handle
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()

# Vercel expects a handler named `app`
app = handle(application)
