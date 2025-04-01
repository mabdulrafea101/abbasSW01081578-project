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
    max_attendees = models.PositiveIntegerField(default=1)  # Quota set by manager
    organizers = models.ManyToManyField(User, through='Application', related_name='events')
    organizers_type = models.CharField(max_length=50, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ], default='teacher')
    event_for = models.CharField(max_length=50, choices=[
        ('student_only', 'Student Only'),
        ('teacher_only', 'Teacher Only'),
        ('everyone', 'Everyone'),
    ], default='student_only')
    event_type = models.CharField(max_length=50, choices=[
        ('online', 'Online'),
        ('physical', 'Physical'),
    ], default='physical')
    is_done = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Application(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apply_as = models.CharField(max_length=50, choices=[
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
        ('attendee', 'Attendee'),
    ], default='attendee')
    apply_date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"
