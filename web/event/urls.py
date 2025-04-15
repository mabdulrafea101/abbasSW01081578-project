from django.urls import path
from .views import (
    AddEventOrganizerView,
    EventCategoryCreateView,
    EventCategoryUpdateView,
    EventCategoryListView,
    EventCategoryDetailView,
    EventCategoryDeleteView,
    EventCreateView,
    EventListView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    ParticipateEventView,
    ParticipatingEventsListView,
    UnparticipateEventView,

)

urlpatterns = [
    # Event Category URLs
    path('categories/', EventCategoryListView.as_view(), name='event_category_list'),
    path('categories/create/', EventCategoryCreateView.as_view(), name='event_category_create'),
    path('categories/<int:pk>/', EventCategoryDetailView.as_view(), name='event_category_detail'),
    path('categories/update/<int:pk>/', EventCategoryUpdateView.as_view(), name='event_category_update'),
    path('categories/delete/<int:pk>/', EventCategoryDeleteView.as_view(), name='event_category_delete'),

    # Event URLs
    path('', EventListView.as_view(), name='event_list'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),

    # Event Organizer URLs
    path('<int:pk>/add-organizer/', AddEventOrganizerView.as_view(), name='event_add_organizer'),

    # Event Participation URLs
    path('participate/<int:pk>/', ParticipateEventView.as_view(), name='event_participate'),
    path('unparticipate/<int:pk>/', UnparticipateEventView.as_view(), name='event_unparticipate'),
    path('participating/', ParticipatingEventsListView.as_view(), name='participating_events'),

]