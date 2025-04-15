from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import CustomUser
from event.models import Event, EventOrganizer, EventParticipant


class OrganizerRating(models.Model):
    """
    Model for storing ratings given by participants to event organizers
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ratings')
    organizer = models.ForeignKey(EventOrganizer, on_delete=models.CASCADE, related_name='ratings')
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('event', 'organizer', 'participant')  # Ensure one rating per organizer per participant per event
        
    def __str__(self):
        return f"{self.participant.username} rated {self.organizer.user.username} {self.rating} stars for {self.event.title}"


class OrganizerComment(models.Model):
    """
    Model for storing comments on organizers by participants
    """
    rating = models.ForeignKey(OrganizerRating, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.rating.participant.username} on {self.rating.organizer.user.username}"


class CommentReply(models.Model):
    """
    Model for storing replies to comments
    """
    comment = models.ForeignKey(OrganizerComment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reply by {self.user.username} to comment #{self.comment.id}"
