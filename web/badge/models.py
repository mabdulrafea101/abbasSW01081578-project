# In badge/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser
from event.models import Event, EventOrganizer, EventParticipant
from review.models import OrganizerRating


class BadgeType(models.Model):
    """Model to store different types of badges"""
    CATEGORY_CHOICES = [
        ('organizer', 'Organizer Badge'),
        ('participant', 'Participant Badge'),
        ('helper', 'Helper Badge'),
    ]
    
    LEVEL_CHOICES = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=20, help_text="Emoji or icon code for the badge")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    requirement_count = models.IntegerField(help_text="Number of actions required to earn this badge")
    
    def __str__(self):
        return f"{self.icon} {self.name} (Level {self.level})"


class UserBadge(models.Model):
    """Model to track badges earned by users"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.ForeignKey(BadgeType, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge_type')
        
    def __str__(self):
        return f"{self.user.username} - {self.badge_type.name}"


class BadgeProgress(models.Model):
    """Model to track progress towards earning badges"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='badge_progress')
    badge_type = models.ForeignKey(BadgeType, on_delete=models.CASCADE)
    current_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'badge_type')
        
    def __str__(self):
        return f"{self.user.username} - {self.badge_type.name}: {self.current_count}/{self.badge_type.requirement_count}"
