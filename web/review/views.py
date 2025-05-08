from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Avg

from .models import OrganizerRating, OrganizerComment, CommentReply
from .forms import OrganizerRatingForm, CommentForm, ReplyForm
from event.models import Event, EventOrganizer, EventParticipant


class EventRatingView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """View to display an event's organizers and their ratings"""
    model = Event
    template_name = 'review/event_rating.html'
    context_object_name = 'event'
    
    def test_func(self):
        event = self.get_object()
        # Allow both participants and organizers to see the rating page
        is_participant = EventParticipant.objects.filter(event=event, user=self.request.user).exists()
        is_organizer = EventOrganizer.objects.filter(event=event, user=self.request.user).exists()
        return is_participant or is_organizer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Get all organizers for this event with their average ratings
        organizers = EventOrganizer.objects.filter(event=event)
        organizer_data = []
        
        for organizer in organizers:
            # Get or initialize a rating form for this organizer
            user_rating = OrganizerRating.objects.filter(
                event=event, 
                organizer=organizer,
                participant=self.request.user
            ).first()
            
            # Calculate average rating
            avg_rating = OrganizerRating.objects.filter(
                event=event, 
                organizer=organizer
            ).aggregate(Avg('rating'))['rating__avg'] or 0
            
            # Initialize form with existing rating or empty
            initial_data = {}
            if user_rating:
                initial_data = {'rating': user_rating.rating}
                
            rating_form = OrganizerRatingForm(instance=user_rating, initial=initial_data)
            
            # Get all comments for this organizer
            comments = OrganizerComment.objects.filter(
                rating__event=event,
                rating__organizer=organizer
            ).order_by('-created_at')
            
            organizer_data.append({
                'organizer': organizer,
                'rating_form': rating_form,
                'average_rating': round(avg_rating, 1),
                'user_rating': user_rating,
                'comments': comments,
                'comment_form': CommentForm(),
            })
        # Check if the current user is an organizer of this event
        is_organizer = EventOrganizer.objects.filter(
            event=event, 
            user=self.request.user
        ).exists()
        
        context['is_organizer'] = is_organizer
            
        context['organizer_data'] = organizer_data
        context['reply_form'] = ReplyForm()
        return context


class RateOrganizerView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to submit a rating for an organizer"""
    model = OrganizerRating
    form_class = OrganizerRatingForm
    http_method_names = ['post']  # Only allow POST requests
    
    def test_func(self):
        # Only participants can rate organizers
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        return EventParticipant.objects.filter(event=event, user=self.request.user).exists()
    
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_pk'])
        organizer = get_object_or_404(EventOrganizer, pk=self.kwargs['organizer_pk'])
        
        # Check if user already rated this organizer
        existing_rating = OrganizerRating.objects.filter(
            event=event,
            organizer=organizer,
            participant=self.request.user
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = form.cleaned_data['rating']
            existing_rating.save()
            
            # Handle comment if provided
            comment_text = form.cleaned_data.get('comment')
            if comment_text:
                OrganizerComment.objects.create(
                    rating=existing_rating,
                    text=comment_text
                )
                
            messages.success(self.request, "Your rating has been updated!")
        else:
            # Create new rating
            rating = form.save(commit=False)
            rating.event = event
            rating.organizer = organizer
            rating.participant = self.request.user
            rating.save()
            
            # Handle comment via form's save method
            form.save()
            
            messages.success(self.request, "Your rating has been submitted!")
            
        return redirect('event_rating', pk=event.pk)
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission. Please try again.")
        return redirect('event_rating', pk=self.kwargs['event_pk'])


class AddCommentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to add a comment to an existing rating"""
    model = OrganizerComment
    form_class = CommentForm
    http_method_names = ['post']
    
    def test_func(self):
        # Only participants can add comments
        rating = get_object_or_404(OrganizerRating, pk=self.kwargs['rating_pk'])
        return rating.participant == self.request.user
    
    def form_valid(self, form):
        rating = get_object_or_404(OrganizerRating, pk=self.kwargs['rating_pk'])
        
        comment = form.save(commit=False)
        comment.rating = rating
        comment.save()
        
        messages.success(self.request, "Your comment has been added!")
        return redirect('event_rating', pk=rating.event.pk)


class AddReplyView(LoginRequiredMixin, CreateView):
    """View to add a reply to a comment"""
    model = CommentReply
    form_class = ReplyForm
    http_method_names = ['post']
    
    def form_valid(self, form):
        comment = get_object_or_404(OrganizerComment, pk=self.kwargs['comment_pk'])
        
        reply = form.save(commit=False)
        reply.comment = comment
        reply.user = self.request.user
        reply.save()
        
        messages.success(self.request, "Your reply has been added!")
        return redirect('event_rating', pk=comment.rating.event.pk)


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a comment"""
    model = OrganizerComment
    
    def test_func(self):
        # Only the comment author can delete it
        comment = self.get_object()
        return comment.rating.participant == self.request.user
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse('event_rating', kwargs={'pk': comment.rating.event.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your comment has been deleted!")
        return super().delete(request, *args, **kwargs)


class DeleteReplyView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a reply"""
    model = CommentReply
    
    def test_func(self):
        # Only the reply author can delete it
        reply = self.get_object()
        return reply.user == self.request.user
    
    def get_success_url(self):
        reply = self.get_object()
        return reverse('event_rating', kwargs={'pk': reply.comment.rating.event.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your reply has been deleted!")
        return super().delete(request, *args, **kwargs)


class UserRatingsListView(LoginRequiredMixin, ListView):
    """View to display all ratings given by the current user"""
    model = OrganizerRating
    template_name = 'review/user_ratings.html'
    context_object_name = 'ratings'
    
    def get_queryset(self):
        return OrganizerRating.objects.filter(
            participant=self.request.user
        ).order_by('-created_at')
