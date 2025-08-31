import os
from alx_travel_app.alx_travel_app.celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("alx_travel_app")

# Load from Django settings with CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py inside apps
app.autodiscover_tasks()
