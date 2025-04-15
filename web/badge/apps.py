# In badge/apps.py
from django.apps import AppConfig

class BadgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'badge'
    
    def ready(self):
        import badge.signals
