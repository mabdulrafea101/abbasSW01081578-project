# Fix the datetime import in models.py
from django.utils import timezone  # Use Django's timezone instead of datetime.timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EventCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='events')
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True) 
    max_organizers = models.PositiveIntegerField(default=1)  # Quota set by manager
    max_participants = models.PositiveIntegerField(default=0)  # Quota set by manager
    event_type = models.CharField(max_length=50, choices=[
        ('online', 'Online'),
        ('physical', 'Physical'),
    ], default='physical')
    is_done = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('upcoming', 'Upcoming'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        default='upcoming'
    )

    def __str__(self):
        return self.title
    
    @property
    def status_badge(self):
        """Return the appropriate badge color based on status"""
        badges = {
            'upcoming': 'info',
            'ongoing': 'primary',
            'completed': 'success',
            'canceled': 'danger'
        }
        return badges.get(self.status, 'secondary')
    
    def update_status(self):
        """Update the event status based on start and end dates"""
        now = timezone.now()
        
        # Skip if the event is already canceled
        if self.status == 'canceled':
            return False
            
        # Check if the event should be marked as completed
        if now > self.end_date_time:
            if self.status != 'completed':
                self.status = 'completed'
                self.save()
                return True
                
        # Check if the event should be marked as ongoing
        elif now >= self.start_date_time and now <= self.end_date_time:
            if self.status != 'ongoing':
                self.status = 'ongoing'
                self.save()
                return True
                
        # Check if the event should be marked as upcoming
        elif now < self.start_date_time:
            if self.status != 'upcoming':
                self.status = 'upcoming'
                self.save()
                return True
                
        return False


class EventOrganizer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='organizers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizing_events')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')  # Prevent duplicate assignments
        
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participating_events')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')  # Prevent duplicate participation
        
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"



