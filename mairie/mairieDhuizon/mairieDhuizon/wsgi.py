import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mairieDhuizon.settings')

#l'application WSGI qui sera utiliser par le serveur web pour gerer les requetes entrant
application = get_wsgi_application()
