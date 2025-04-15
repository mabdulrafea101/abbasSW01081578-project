from django.core.management.base import BaseCommand
from event.models import Event
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates all event statuses'

    def handle(self, *args, **options):
        events = Event.objects.all()
        updated_count = 0
        
        for event in events:
            if event.update_status():  # Using the model method
                updated_count += 1
                
        self.stdout.write(
            self.style.SUCCESS(f'Updated {updated_count} event statuses')
        )
        
        return updated_count
