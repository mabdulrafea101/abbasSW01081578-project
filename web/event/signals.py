from django.dispatch import Signal, receiver
from django.utils import timezone
from .models import Event

# Create a custom signal
event_view_accessed = Signal()

@receiver(event_view_accessed)
def update_event_statuses(sender, **kwargs):
    """
    Signal handler to update event statuses when event views are accessed
    """
    events = Event.objects.all()
    updated_count = 0
    
    for event in events:
        if event.update_status():  # Use the existing model method
            updated_count += 1
            
    return updated_count
