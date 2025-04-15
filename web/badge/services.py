# In badge/services.py
from django.db.models import Count
from django.utils import timezone
from .models import BadgeType, UserBadge, BadgeProgress
from event.models import EventOrganizer, EventParticipant
from review.models import OrganizerRating


def update_organizer_badges(user):
    """Update organizer badges based on events hosted"""
    # Count events organized by the user
    events_count = EventOrganizer.objects.filter(user=user).count()
    
    # Check for each badge level
    organizer_badges = BadgeType.objects.filter(category='organizer').order_by('level')
    
    for badge in organizer_badges:
        # Get or create progress record
        progress, created = BadgeProgress.objects.get_or_create(
            user=user,
            badge_type=badge,
            defaults={'current_count': events_count}
        )
        
        # Update progress if not created
        if not created:
            progress.current_count = events_count
            progress.save()
            
        # Check if badge should be awarded
        if events_count >= badge.requirement_count:
            UserBadge.objects.get_or_create(user=user, badge_type=badge)


def update_participant_badges(user):
    """Update participant badges based on events attended"""
    # Count events participated in
    events_count = EventParticipant.objects.filter(user=user).count()
    
    # Check for each badge level
    participant_badges = BadgeType.objects.filter(category='participant').order_by('level')
    
    for badge in participant_badges:
        # Get or create progress record
        progress, created = BadgeProgress.objects.get_or_create(
            user=user,
            badge_type=badge,
            defaults={'current_count': events_count}
        )
        
        # Update progress if not created
        if not created:
            progress.current_count = events_count
            progress.save()
            
        # Check if badge should be awarded
        if events_count >= badge.requirement_count:
            UserBadge.objects.get_or_create(user=user, badge_type=badge)


def update_helper_badges(user):
    """Update helper badges based on ratings given"""
    # Count ratings given by the user
    ratings_count = OrganizerRating.objects.filter(participant=user).count()
    
    # Check for each badge level
    helper_badges = BadgeType.objects.filter(category='helper').order_by('level')
    
    for badge in helper_badges:
        # Get or create progress record
        progress, created = BadgeProgress.objects.get_or_create(
            user=user,
            badge_type=badge,
            defaults={'current_count': ratings_count}
        )
        
        # Update progress if not created
        if not created:
            progress.current_count = ratings_count
            progress.save()
            
        # Check if badge should be awarded
        if ratings_count >= badge.requirement_count:
            UserBadge.objects.get_or_create(user=user, badge_type=badge)


def update_all_badges(user):
    """Update all badge types for a user"""
    update_organizer_badges(user)
    update_participant_badges(user)
    update_helper_badges(user)
