# In badge/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from event.models import EventOrganizer, EventParticipant
from review.models import OrganizerRating
from .services import update_organizer_badges, update_participant_badges, update_helper_badges

@receiver(post_save, sender=EventOrganizer)
def handle_event_organizer_created(sender, instance, created, **kwargs):
    """Update organizer badges when a user is assigned as an event organizer"""
    if created:
        update_organizer_badges(instance.user)

@receiver(post_save, sender=EventParticipant)
def handle_event_participant_created(sender, instance, created, **kwargs):
    """Update participant badges when a user participates in an event"""
    if created:
        update_participant_badges(instance.user)

@receiver(post_save, sender=OrganizerRating)
def handle_organizer_rating_created(sender, instance, created, **kwargs):
    """Update helper badges when a user rates an organizer"""
    if created:
        update_helper_badges(instance.participant)
