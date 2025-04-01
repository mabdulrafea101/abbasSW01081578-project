from django.urls import path
from .views import (
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
    ApplicationCreateView,
    ApplicationListView,
    ApplicationUpdateView,

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

    # Application URLs
    path('applications/create/', ApplicationCreateView.as_view(), name='organizer_application_create'),
    path('applications/', ApplicationListView.as_view(), name='organizer_application_list'),
    path('applications/update/<int:pk>/', ApplicationUpdateView.as_view(), name='organizer_application_update'),
]
