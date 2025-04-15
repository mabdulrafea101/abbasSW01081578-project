# In badge/admin.py
from django.contrib import admin
from .models import BadgeType, UserBadge, BadgeProgress

@admin.register(BadgeType)
class BadgeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'category', 'level', 'requirement_count')
    list_filter = ('category', 'level')
    search_fields = ('name', 'description')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_type', 'earned_at')
    list_filter = ('badge_type__category', 'badge_type__level')
    search_fields = ('user__username', 'badge_type__name')
    date_hierarchy = 'earned_at'

@admin.register(BadgeProgress)
class BadgeProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_type', 'current_count', 'last_updated')
    list_filter = ('badge_type__category', 'badge_type__level')
    search_fields = ('user__username', 'badge_type__name')

