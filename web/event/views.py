from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from user.mixins import ManagerRequiredMixin
from .models import Event, EventCategory, OrganizerApplication
from .forms import EventForm, EventCategoryForm, OrganizerApplicationForm
from django.contrib import messages


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
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/event_list.html'
    context_object_name = 'events'


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/event_detail.html'


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


class OrganizerApplicationCreateView(LoginRequiredMixin, CreateView):
    model = OrganizerApplication
    form_class = OrganizerApplicationForm
    template_name = 'event/organizer_application_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Application submitted successfully!')
        return super().form_valid(form)


class OrganizerApplicationListView(LoginRequiredMixin, ListView):
    model = OrganizerApplication
    template_name = 'event/organizer_application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return OrganizerApplication.objects.filter(event__organizers=self.request.user)


class OrganizerApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = OrganizerApplication
    form_class = OrganizerApplicationForm
    template_name = 'event/organizer_application_form.html'
    success_url = reverse_lazy('organizer_application_list')

    def form_valid(self, form):
        messages.success(self.request, 'Application status updated successfully!')
        return super().form_valid(form)
