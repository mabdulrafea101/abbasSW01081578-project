# In badge/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from event.models import EventParticipant, EventOrganizer
from review.models import OrganizerRating
from .services import update_participant_badge_progress, update_helper_badge_progress, update_organizer_badge_progress

@receiver(post_save, sender=EventParticipant)
@receiver(post_delete, sender=EventParticipant)
def update_badges_on_participation_change(sender, instance, **kwargs):
    """
    Update badge progress when a user joins or leaves an event
    """
    user = instance.user
    update_participant_badge_progress(user)

@receiver(post_save, sender=EventOrganizer)
@receiver(post_delete, sender=EventOrganizer)
def update_badges_on_organizer_change(sender, instance, **kwargs):
    """
    Update badge progress when a user becomes or stops being an event organizer
    """
    user = instance.user
    update_organizer_badge_progress(user)

@receiver(post_save, sender=OrganizerRating)
@receiver(post_delete, sender=OrganizerRating)
def update_badges_on_rating_change(sender, instance, **kwargs):
    """
    Update badge progress when a user rates or removes a rating for an organizer
    """
    participant = instance.participant
    update_helper_badge_progress(participant)
