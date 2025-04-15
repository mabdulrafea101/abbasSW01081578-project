# In review/forms.py
from django import forms
from .models import OrganizerRating, OrganizerComment, CommentReply


class OrganizerRatingForm(forms.ModelForm):
    """Form for rating an event organizer"""
    
    class Meta:
        model = OrganizerRating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f"{i} Stars") for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
        }
        
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Share your thoughts about this organizer...'
        }),
        required=False
    )
    
    def save(self, commit=True):
        rating = super().save(commit=commit)
        
        # If there's a comment, create it
        comment_text = self.cleaned_data.get('comment')
        if comment_text and commit:
            OrganizerComment.objects.create(
                rating=rating,
                text=comment_text
            )
            
        return rating


class CommentForm(forms.ModelForm):
    """Form for adding a comment to a rating"""
    
    class Meta:
        model = OrganizerComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Add your comment...'
            }),
        }


class ReplyForm(forms.ModelForm):
    """Form for replying to a comment"""
    
    class Meta:
        model = CommentReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'Add your reply...'
            }),
        }