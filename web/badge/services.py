# In badge/services.py
from django.db.models import Count
from .models import BadgeType, UserBadge, BadgeProgress
from event.models import EventParticipant, EventOrganizer
from review.models import OrganizerRating

def update_participant_badge_progress(user):
    """Update the badge progress for participant-related badges"""
    # Get all participant-related badge types
    badges = BadgeType.objects.filter(category='participant')
    
    # Count the number of events the user has participated in
    participation_count = EventParticipant.objects.filter(user=user).count()
    
    # Update progress for each badge type
    for badge in badges:
        progress, created = BadgeProgress.objects.get_or_create(
            user=user,
            badge_type=badge,
            defaults={'current_count': 0}
        )
        
        # Update the current count
        progress.current_count = participation_count
        progress.save()
        
        # Check if the badge should be awarded
        if (participation_count >= badge.requirement_count and 
            not UserBadge.objects.filter(user=user, badge_type=badge).exists()):
            UserBadge.objects.create(user=user, badge_type=badge)

def update_helper_badge_progress(user):
    """Update the badge progress for helper-related badges (ratings)"""
    # Get all helper-related badge types
    badges = BadgeType.objects.filter(category='helper')
    
    # Count the number of organizers the user has rated
    rating_count = OrganizerRating.objects.filter(participant=user).count()
    
    # Update progress for each badge type
    for badge in badges:
        progress, created = BadgeProgress.objects.get_or_create(
            user=user,
            badge_type=badge,
            defaults={'current_count': 0}
        )
        
        # Update the current count
        progress.current_count = rating_count
        progress.save()
        
        # Check if the badge should be awarded
        if (rating_count >= badge.requirement_count and 
            not UserBadge.objects.filter(user=user, badge_type=badge).exists()):
            UserBadge.objects.create(user=user, badge_type=badge)

def update_organizer_badge_progress(user):
    """Update the badge progress for organizer-related badges"""
    # Get all organizer-related badge types
    badges = BadgeType.objects.filter(category='organizer')
    
    # Count the number of events the user has organized
    organizer_count = EventOrganizer.objects.filter(user=user).count()
    
    # Update progress for each badge type
    for badge in badges:
        progress, created = BadgeProgress.objects.get_or_create(
            user=user,
            badge_type=badge,
            defaults={'current_count': 0}
        )
        
        # Update the current count
        progress.current_count = organizer_count
        progress.save()
        
        # Check if the badge should be awarded
        if (organizer_count >= badge.requirement_count and 
            not UserBadge.objects.filter(user=user, badge_type=badge).exists()):
            UserBadge.objects.create(user=user, badge_type=badge)

def update_all_badges(user):
    """Update all badge progress and awards for a user"""
    update_participant_badge_progress(user)
    update_helper_badge_progress(user)
    update_organizer_badge_progress(user)
