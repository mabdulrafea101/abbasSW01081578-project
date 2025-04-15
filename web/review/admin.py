from django.contrib import admin
from .models import OrganizerRating, OrganizerComment, CommentReply

# Register your models here.


class OrganizerRatingAdmin(admin.ModelAdmin):
    list_display = ('event', 'organizer', 'participant', 'rating')
    list_filter = ('event', 'organizer', 'rating')
    search_fields = ('event__title', 'organizer__user__username', 'participant__username')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        return False  # Prevent adding reviews directly from the admin
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting reviews directly from the admin
    
    def has_change_permission(self, request, obj=None):
        return False  # Prevent changing reviews directly from the admin
    
    def has_view_permission(self, request, obj=None):
        return True  # Allow viewing reviews in the admin


class OrganizerCommentAdmin(admin.ModelAdmin):
    list_display = ('rating', 'get_participant', 'get_organizer', 'text_preview')
    list_filter = ('rating__event', 'rating__organizer')
    search_fields = ('rating__event__title', 'rating__participant__username', 'text')
    ordering = ('-created_at',)
    
    def get_participant(self, obj):
        return obj.rating.participant.username
    get_participant.short_description = 'Participant'
    
    def get_organizer(self, obj):
        return obj.rating.organizer.user.username
    get_organizer.short_description = 'Organizer'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'
    
    def has_add_permission(self, request):
        return False  # Prevent adding comments directly from the admin
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting comments directly from the admin
    
    def has_change_permission(self, request, obj=None):
        return False  # Prevent changing comments directly from the admin
    
    def has_view_permission(self, request, obj=None):
        return True  # Allow viewing comments in the admin


class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ('get_comment_text', 'user', 'text_preview')
    list_filter = ('comment__rating__event', 'user')
    search_fields = ('comment__rating__event__title', 'user__username', 'text')
    ordering = ('-created_at',)
    
    def get_comment_text(self, obj):
        return obj.comment.text[:30] + '...' if len(obj.comment.text) > 30 else obj.comment.text
    get_comment_text.short_description = 'Reply to'
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Reply text'
    
    def has_add_permission(self, request):
        return False  # Prevent adding replies directly from the admin
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deleting replies directly from the admin
    
    def has_change_permission(self, request, obj=None):
        return False  # Prevent changing replies directly from the admin
    
    def has_view_permission(self, request, obj=None):
        return True  # Allow viewing replies in the admin


admin.site.register(OrganizerRating, OrganizerRatingAdmin)
admin.site.register(OrganizerComment, OrganizerCommentAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)