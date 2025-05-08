from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

from event.models import EventParticipant, EventOrganizer, Event
from review.models import OrganizerRating

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@receiver(post_save, sender=CustomUser)
def set_superuser_fields(sender, instance, created, **kwargs):
    """
    Signal to automatically set user_type to 'manager' and is_account_confirmed to True 
    for superusers upon creation or when superuser status is granted.
    Also ensures the superuser has a profile.
    """
    if instance.is_superuser:
        # Check if user_type or is_account_confirmed needs to be updated
        update_fields = []
        
        if instance.user_type != 'manager':
            instance.user_type = 'manager'
            update_fields.append('user_type')
            
        if not instance.is_account_confirmed:
            instance.is_account_confirmed = True
            update_fields.append('is_account_confirmed')
            
        # Only save if there are fields to update, and use update_fields to avoid infinite signal loop
        if update_fields:
            # Disconnect the signal temporarily to avoid infinite recursion
            post_save.disconnect(set_superuser_fields, sender=CustomUser)
            instance.save(update_fields=update_fields)
            # Reconnect the signal
            post_save.connect(set_superuser_fields, sender=CustomUser)
        
        # Check if profile exists, create if it doesn't
        try:
            instance.profile
        except Profile.RelatedObjectDoesNotExist:
            # Create profile if it doesn't exist
            Profile.objects.create(user=instance)


@receiver(post_save, sender=EventParticipant)
def award_participation_points(sender, instance, created, **kwargs):
    """Award points when a user participates in an event"""
    if created:
        user = instance.user
        event = instance.event
        user.profile.add_points(2, f"Participated in event: {event.title}")


@receiver(post_save, sender=Event)
def award_organizer_points_on_completion(sender, instance, **kwargs):
    """Award points to organizers when an event is completed"""
    if instance.status == 'completed':
        for organizer in instance.organizers.all():
            organizer.user.profile.add_points(3, f"Organized completed event: {instance.title}")


@receiver(post_save, sender=OrganizerRating)
def award_rating_points(sender, instance, created, **kwargs):
    """Award points for submitting and receiving ratings"""
    if created:
        # Award points to the participant for submitting a rating
        participant = instance.participant
        participant.profile.add_points(1, f"Rated organizer in event: {instance.event.title}")
        
        # Award points to the organizer based on rating value
        organizer = instance.organizer.user
        rating_value = instance.rating
        organizer.profile.add_points(
            rating_value, 
            f"Received {rating_value}-star rating in event: {instance.event.title}"
        )



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance when a CustomUser is created.
    """
    if created:
        Profile.objects.create(user=instance)



@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile instance when the CustomUser is saved.
    """
    try:
        instance.profile.save()
    except AttributeError:
        # Create profile if it doesn't exist
        Profile.objects.create(user=instance)


# In user/signals.py
# @receiver(post_save, sender=Profile)
# def notify_level_up(sender, instance, **kwargs):
#     """Send notification when a user levels up"""
#     if instance.tracker.has_changed('current_level') and instance.tracker.previous('current_level'):
#         old_level = instance.tracker.previous('current_level')
#         new_level = instance.current_level
        
#         if new_level > old_level:
#             # Create a notification
#             Notification.objects.create(
#                 user=instance.user,
#                 title="Level Up!",
#                 message=f"Congratulations! You've advanced to level {new_level}.",
#                 notification_type="achievement"
#             )
