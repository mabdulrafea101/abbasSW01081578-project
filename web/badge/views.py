# In badge/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import BadgeType, UserBadge, BadgeProgress
from .services import update_all_badges
from user.models import CustomUser


class UserBadgesView(LoginRequiredMixin, ListView):
    """View to display all badges earned by the current user"""
    model = UserBadge
    template_name = 'badge/user_badges.html'
    context_object_name = 'badges'
    
    def get_queryset(self):
        # Update badges before displaying
        update_all_badges(self.request.user)
        
        # Return the user's badges sorted by category and level
        return UserBadge.objects.filter(user=self.request.user).select_related('badge_type').order_by(
            'badge_type__category', 'badge_type__level'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group badges by category for easy display
        badges_by_category = {}
        for category, label in BadgeType.CATEGORY_CHOICES:
            category_badges = self.get_queryset().filter(badge_type__category=category)
            badges_by_category[category] = {
                'label': label,
                'badges': category_badges
            }
        
        context['badges_by_category'] = badges_by_category
        
        # Get progress for badges not yet earned
        earned_badge_types = UserBadge.objects.filter(user=self.request.user).values_list(
            'badge_type_id', flat=True)
        
        in_progress_badges = BadgeProgress.objects.filter(
            user=self.request.user
        ).exclude(
            badge_type_id__in=earned_badge_types
        ).select_related('badge_type')
        
        # Group in-progress badges by category
        progress_by_category = {}
        for category, label in BadgeType.CATEGORY_CHOICES:
            category_progress = in_progress_badges.filter(badge_type__category=category)
            progress_by_category[category] = {
                'label': label,
                'items': category_progress
            }
        
        context['progress_by_category'] = progress_by_category
        
        return context


class AllBadgesView(LoginRequiredMixin, ListView):
    """View to display all available badges in the system"""
    model = BadgeType
    template_name = 'badge/all_badges.html'
    context_object_name = 'badges'
    
    def get_queryset(self):
        return BadgeType.objects.all().order_by('category', 'level')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group badges by category for easy display
        badges_by_category = {}
        for category, label in BadgeType.CATEGORY_CHOICES:
            category_badges = self.get_queryset().filter(category=category)
            badges_by_category[category] = {
                'label': label,
                'badges': category_badges
            }
        
        context['badges_by_category'] = badges_by_category
        
        # Get user's earned badges
        if self.request.user.is_authenticated:
            earned_badges = UserBadge.objects.filter(
                user=self.request.user
            ).values_list('badge_type_id', flat=True)
            
            # Get user's progress
            progress = BadgeProgress.objects.filter(
                user=self.request.user
            ).select_related('badge_type')
            
            progress_dict = {p.badge_type_id: p.current_count for p in progress}
            
            context['earned_badges'] = earned_badges
            context['badge_progress'] = progress_dict
        
        return context


class UserProfileBadgesView(LoginRequiredMixin, DetailView):
    """View to display badges earned by a specific user"""
    model = CustomUser
    template_name = 'badge/user_profile_badges.html'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Get badges earned by the user
        badges = UserBadge.objects.filter(user=user).select_related('badge_type').order_by(
            'badge_type__category', 'badge_type__level'
        )
        
        # Group badges by category
        badges_by_category = {}
        for category, label in BadgeType.CATEGORY_CHOICES:
            category_badges = badges.filter(badge_type__category=category)
            badges_by_category[category] = {
                'label': label,
                'badges': category_badges
            }
        
        context['badges_by_category'] = badges_by_category
        return context
