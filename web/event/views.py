from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from user.mixins import ManagerRequiredMixin
from .models import Event, EventCategory, EventOrganizer, EventParticipant
from review.models import OrganizerRating
from .forms import AddOrganizerForm, EventForm, EventCategoryForm
from django.contrib import messages

from django.core.management import call_command
from .signals import event_view_accessed


# Replace the refresh_event_statuses function with:
def refresh_event_statuses():
    """Emit signal to update event statuses and return count of updated events"""
    return event_view_accessed.send(sender=EventListView)[0][1]


# EventCategory CRUD Views
class EventCategoryListView(LoginRequiredMixin, ListView):
    model = EventCategory
    template_name = 'event/event_category_list.html'
    context_object_name = 'categories'


class EventCategoryDetailView(LoginRequiredMixin, DetailView):
    model = EventCategory
    template_name = 'event/event_category_detail.html'


class EventCategoryCreateView(ManagerRequiredMixin, CreateView):
    model = EventCategory
    form_class = EventCategoryForm
    template_name = 'event/event_category_form.html'
    success_url = reverse_lazy('event_category_list')


class EventCategoryUpdateView(ManagerRequiredMixin, UpdateView):
    model = EventCategory
    form_class = EventCategoryForm
    template_name = 'event/event_category_form.html'
    success_url = reverse_lazy('event_category_list')


class EventCategoryDeleteView(ManagerRequiredMixin, DeleteView):
    model = EventCategory
    template_name = 'event/event_category_confirm_delete.html'
    success_url = reverse_lazy('event_category_list')


# Event CRUD Views
# In event/views.py
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'
    ordering = ['-start_date_time']

    def get(self, request, *args, **kwargs):
        # Send signal to update event statuses
        event_view_accessed.send(sender=self.__class__)
        # Continue with normal processing
        return super().get(request, *args, **kwargs)
     
    def get_queryset(self):
        # Run the command to update all event statuses
        refresh_event_statuses()
        
        # Get the events
        return super().get_queryset()


# In event/views.py
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/event_detail.html'

    def get_object(self, queryset=None):
        # Run the command to update all event statuses
        refresh_event_statuses()
        
        # Get the event object
        event = super().get_object(queryset)
        return event
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add participating flag for students
        if self.request.user.user_type == 'student':
            context['is_participating'] = EventParticipant.objects.filter(
                event=self.object, 
                user=self.request.user
            ).exists()
        return context


class EventCreateView(ManagerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event_list')




class EventUpdateView(ManagerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event/event_form.html'
    success_url = reverse_lazy('event_list')


class EventDeleteView(ManagerRequiredMixin, DeleteView):
    model = Event
    template_name = 'event/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')


# Add Organizer View

class AddEventOrganizerView(ManagerRequiredMixin, FormView):
    template_name = 'event/add_organizer.html'
    form_class = AddOrganizerForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.event = get_object_or_404(Event, pk=self.kwargs['pk'])
        kwargs['event'] = self.event
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        context['current_organizers'] = self.event.organizers.all()
        context['organizer_count'] = self.event.organizers.count()
        context['max_organizers'] = self.event.max_organizers
        return context
    
    def form_valid(self, form):
        event = self.event
        user = form.cleaned_data['organizer']
        
        # Create the organizer relationship
        EventOrganizer.objects.create(event=event, user=user)
        
        messages.success(self.request, f"{user.username} has been added as an organizer for {event.title}.")
        return redirect('event_detail', pk=event.pk)


class EventOrganizerDeleteView(ManagerRequiredMixin, DeleteView):
    model = EventOrganizer
    template_name = 'event/event_organizer_confirm_delete.html'
    success_url = reverse_lazy('event_list')
    context_object_name = 'event_organizer'

    # Override the get_object method to get the EventOrganizer instance
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.event = obj.event
        return obj
    
    # Override the get_context_data method to pass the event to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context
    
    # Override the form_valid method to show a success message
    def form_valid(self, form):
        messages.success(self.request, f"{self.object.user.username} has been removed as an organizer for {self.event.title}.")
        return super().form_valid(form)
    

class ParticipateEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    """View to allow students to participate in an event"""
    
    def test_func(self):
        # Only students can participate in events
        return self.request.user.user_type == 'student'
        
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

         # Check if the event's status allows participation
        if event.status not in ['upcoming']:
            messages.error(request, f"You cannot participate in an event with status: {event.get_status_display()}")
            return redirect('event_detail', pk=event.pk)
        
        # Check if the event is already full
        if event.max_participants and event.participants.count() >= event.max_participants:
            messages.error(request, "This event has reached its maximum number of participants.")
            return redirect('event_detail', pk=event.pk)
            
        # Check if the event's status allows participation
        if event.status not in ['upcoming', 'ongoing']:
            messages.error(request, f"You cannot participate in an event with status: {event.get_status_display()}")
            return redirect('event_detail', pk=event.pk)
            
        # Check if the user is already participating
        if EventParticipant.objects.filter(event=event, user=request.user).exists():
            messages.info(request, f"You are already participating in {event.title}.")
            return redirect('event_detail', pk=event.pk)
        
        if event.status not in ['upcoming', 'ongoing']:
            messages.error(request, f"You cannot participate in an event with status: {event.get_status_display()}")
            return redirect('event_detail', pk=event.pk)
        
        # Check if the user is an organizer of this event
        if EventOrganizer.objects.filter(event=event, user=request.user).exists():
            messages.error(request, "As an organizer of this event, you cannot participate as an attendee.")
            return redirect('event_detail', pk=event.pk)
        

        # Create the participation
        EventParticipant.objects.create(event=event, user=request.user)
        messages.success(request, f"You are now participating in {event.title}.")
        
        return redirect('event_detail', pk=event.pk)


class UnparticipateEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    """View to allow students to withdraw participation from an event"""
    
    def test_func(self):
        # Only students can withdraw from events
        return self.request.user.user_type == 'student'
        
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        # Check if the event's status allows withdrawal
        if event.status == 'completed':
            messages.error(request, "You cannot withdraw from a completed event.")
            return redirect('event_detail', pk=event.pk)
            
        # Find and delete the participation entry
        participation = get_object_or_404(EventParticipant, event=event, user=request.user)
        participation.delete()
        
        messages.success(request, f"You are no longer participating in {event.title}.")
        return redirect('event_detail', pk=event.pk)


# In event/views.py
class ParticipatingEventsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View to display all events a student is participating in"""
    model = Event
    template_name = 'event/participating_events.html'
    context_object_name = 'events'
    
    def test_func(self):
        return self.request.user.user_type == 'student'
    
    def get_queryset(self):
        # Run the status update command
        refresh_event_statuses()
        
        # Get the participating events
        return Event.objects.filter(participants__user=self.request.user)


class UnreviewedCompletedEventsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Display completed events that the participant hasn't reviewed yet"""
    model = Event
    template_name = 'event/unreviewed_events.html'
    context_object_name = 'events'
    
    def test_func(self):
        # Only students can view/rate events
        return self.request.user.user_type == 'student'
    
    def get_queryset(self):
        # Get all completed events where the user is a participant
        user_events = Event.objects.filter(
            participants__user=self.request.user,
            status='completed'
        )
        
        # Filter out events that the user has already rated
        unreviewed_events = []
        for event in user_events:
            # Check if the user has rated any organizer in this event
            has_rated = OrganizerRating.objects.filter(
                event=event,
                participant=self.request.user
            ).exists()
            
            if not has_rated:
                unreviewed_events.append(event)
                
        return unreviewed_events


class ReviewedEventsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Display events that the participant has already reviewed"""
    model = Event
    template_name = 'event/reviewed_events.html'
    context_object_name = 'events'
    
    def test_func(self):
        # Only students can view their reviews
        return self.request.user.user_type == 'student'
    
    def get_queryset(self):
        # Get all events where the user has submitted at least one rating
        rated_event_ids = OrganizerRating.objects.filter(
            participant=self.request.user
        ).values_list('event_id', flat=True).distinct()
        
        # Get the event objects for these IDs
        return Event.objects.filter(id__in=rated_event_ids)
    

class OrganizingEventsListView(LoginRequiredMixin, ListView):
    """View to display all events a user is organizing"""
    model = Event
    template_name = 'event/organizing_events.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        # Run the status update command
        refresh_event_statuses()
        
        # Get events where the user is an organizer
        return Event.objects.filter(organizers__user=self.request.user)
