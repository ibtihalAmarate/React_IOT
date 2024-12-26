import os
import sys

# Ajoutez le chemin de votre projet Django
project_path = '/home/username/REACT_IOT/backend'
if project_path not in sys.path:
    sys.path.append(project_path)

# Configurez l'environnement Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

# Chargez l'application WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
